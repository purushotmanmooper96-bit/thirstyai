// Runs on an isolated CI browser, against the exact built files, without external APIs.
import { chromium } from "playwright";
import { createServer } from "node:http";
import fs from "node:fs/promises";
import path from "node:path";
import assert from "node:assert/strict";
const root = path.resolve("dist");
const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    const file = path.resolve(
      root,
      "." +
        decodeURIComponent(url.pathname === "/" ? "/index.html" : url.pathname),
    );
    if (!file.startsWith(root + path.sep)) throw new Error("Path outside site");
    const mime = {
      ".mjs": "text/javascript",
      ".css": "text/css",
      ".json": "application/json",
      ".html": "text/html",
      ".svg": "image/svg+xml",
      ".png": "image/png",
    };
    res.setHeader(
      "Content-Type",
      mime[path.extname(file)] || "application/octet-stream",
    );
    res.end(await fs.readFile(file));
  } catch {
    res.writeHead(404);
    res.end("Not found");
  }
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const url = `http://127.0.0.1:${server.address().port}/`;
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || "/usr/bin/google-chrome",
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  permissions: ["clipboard-read", "clipboard-write"],
});
const page = await context.newPage();
page.setDefaultTimeout(10000);
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));
const results = [];
async function check(name, fn) {
  await fn();
  results.push({ name, status: "PASS" });
  console.log("PASS", name);
}
try {
  await check("guided first-use page", async () => {
    await page.goto(url);
    await page
      .getByRole("heading", { level: 1, name: /See what AI water/ })
      .waitFor();
    await page.getByRole("link", { name: /Understand one claim/ }).click();
    await page
      .getByRole("heading", { name: "Spot the missing boundary." })
      .waitFor();
    await page.getByRole("button", { name: "No", exact: true }).click();
    assert.match(
      await page.locator("#challenge-answer").innerText(),
      /Correct/,
    );
  });
  await check(
    "invalid lab input blocks stale outputs, share and exports; corrected input recovers",
    async () => {
      await page.goto(url + "#lab");
      await page.locator("#lab-results").waitFor();
      await page.locator("#workload").fill("");
      assert.equal(await page.locator("#lab-results").isVisible(), false);
      for (const id of ["share", "receipt", "export-scenario"])
        assert.equal(await page.locator("#" + id).isDisabled(), true);
      await page.locator("#workload").fill("2000");
      assert.equal(await page.locator("#lab-results").isVisible(), true);
      assert.match(await page.locator("#lab-results").innerText(), /4.40 ML/);
      await page.locator(".advanced-controls summary").click();
      await page.locator("#a-wue-exact").fill("");
      assert.equal(await page.locator("#share").isDisabled(), true);
      await page.locator("#a-wue-exact").fill("0.2");
      assert.equal(await page.locator("#share").isDisabled(), false);
    },
  );
  await check("complete JSON export and PNG receipt", async () => {
    await page.locator(".result-details summary").click();
    const [download] = await Promise.all([
      page.waitForEvent("download"),
      page.locator("#export-scenario").click(),
    ]);
    const obj = JSON.parse(await fs.readFile(await download.path(), "utf8"));
    assert.equal(obj.inputs.baseline.it_mwh, 2000);
    assert.equal(obj.inputs.alternative.wue, 0.2);
    assert.match(obj.warning, /NOT MEASUREMENTS/);
    const [card] = await Promise.all([
      page.waitForEvent("download"),
      page.locator("#receipt").click(),
    ]);
    const bytes = await fs.readFile(await card.path());
    assert.equal(bytes.subarray(1, 4).toString(), "PNG");
    await fs.mkdir("outputs/browser", { recursive: true });
    await fs.writeFile("outputs/browser/result-card.png", bytes);
  });
  await check("scenario link round trip and reset", async () => {
    await page.locator("#share").click();
    const link = await page.evaluate(() => navigator.clipboard.readText());
    await page.goto(link);
    assert.equal(await page.locator("#workload").inputValue(), "2000");
    assert.equal(await page.locator("#a-wue-exact").inputValue(), "0.2");
    await page.locator("#reset").click();
    assert.equal(new URL(page.url()).search, "");
    assert.equal(await page.locator("#workload").inputValue(), "1000");
  });
  await check("company filters, conversions and all locations", async () => {
    await page.goto(url + "#companies");
    await page.locator("#company-filter").selectOption("Microsoft");
    await page.locator("#metric-filter").selectOption("consumption");
    assert.match(await page.locator("#company-count").innerText(), /^1 of/);
    await page.locator("#unit-filter").selectOption("litres");
    assert.match(
      await page.locator("#company-cards").innerText(),
      /8,170,000,000 L/,
    );
    await page.goto(url + "#locations");
    assert.equal(await page.locator("tbody tr").count(), 7);
    assert.match(await page.locator("main").innerText(), /Unknown/);
  });
  await check("desktop and mobile keyboard/overflow", async () => {
    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: 844 });
      for (const route of ["companies", "locations", "challenge", "lab"]) {
        await page.goto(url + "#" + route);
        await page
          .getByRole("link", { name: "Skip to content", exact: true })
          .press("Enter");
        assert.equal(new URL(page.url()).hash, "#" + route);
        assert.equal(
          await page
            .locator("main")
            .evaluate((el) => el === document.activeElement),
          true,
        );
        assert.ok(
          await page.evaluate(
            () =>
              document.documentElement.scrollWidth <=
              document.documentElement.clientWidth,
          ),
        );
      }
    }
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto(url);
    await page.getByRole("heading", { name: /See what AI water/ }).waitFor();
    await page.screenshot({ path: "outputs/browser/overview.png" });
    await page.goto(url + "#lab");
    await page.locator("#lab-results").waitFor();
    await page.screenshot({ path: "outputs/browser/lab.png" });
  });
  await check(
    "evidence failure retains static sources; retry works",
    async () => {
      await page.route("**/data/evidence.json", (route) =>
        route.fulfill({ status: 503, body: "Unavailable" }),
      );
      await page.reload();
      await page.getByText(/Interactive data unavailable/).waitFor();
      assert.equal(
        await page
          .getByRole("heading", { name: "Company water disclosures" })
          .count(),
        1,
      );
      await page.unroute("**/data/evidence.json");
      await page
        .getByRole("button", { name: "Retry interactive view" })
        .click();
      await page
        .getByRole("heading", {
          name: "A better choice depends on the boundary.",
        })
        .waitFor();
    },
  );
  assert.deepEqual(errors, []);
  await fs.writeFile(
    "outputs/browser/report.json",
    JSON.stringify({ results, pageErrors: errors }, null, 2),
  );
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
