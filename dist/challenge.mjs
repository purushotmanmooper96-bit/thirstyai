import { downloadTextCard } from "./sharing.mjs";
export const CHALLENGES = [
  {
    id: "metric",
    ids: ["CORP03", "CORP04"],
    question: "Can withdrawal and consumption be ranked as the same metric?",
    answer: false,
    explanation:
      "No. Withdrawal is water taken from a source. Consumption is the portion not returned within the stated boundary. Different quantities are not a performance ranking.",
  },
  {
    id: "scope",
    ids: ["CORP04", "CORP08"],
    question:
      "Do these consumption totals cover the same fleet and reporting period?",
    answer: false,
    explanation:
      "No. Google reports operational data centres; Microsoft reports enterprise operations including offices and labs. The calendar and fiscal reporting periods differ. A unit conversion would not fix those boundaries.",
  },
  {
    id: "coexist",
    ids: ["CORP13", "CORP14"],
    question:
      "Can the same fleet report both withdrawal and consumption without a contradiction?",
    answer: true,
    explanation:
      "Yes. Both quantities can describe the same operations. They measure different parts of the water account. This does not make them interchangeable or establish local environmental harm.",
  },
];
export function createChallenge({ data, esc, link, toast }) {
  let index = 0;
  let revealed = false;
  function challenge() {
    const q = CHALLENGES[index];
    return `<div class="pagehead"><div class="eyebrow">Claim challenge</div><h1>Spot the missing boundary.</h1><p>Three short questions using published disclosures. This tests accounting definitions, not company ethics.</p></div><article class="card"><p>Question ${index + 1} of ${CHALLENGES.length}</p><h2>${q.question}</h2><div class="pair">${q.ids
      .map((id) => {
        const c = data.companies.find((r) => r.observation_id === id);
        return `<section class="challenge-observation"><h3>${esc(c.company)} · ${esc(c.metric)}</h3><p><strong>${esc(c.value)} ${esc(c.unit)}</strong></p><p>${esc(c.period)} · ${esc(c.geography)}</p><p>${esc(c.scope)}</p><p>${esc(c.water_metric)} · extraction confidence ${esc(c.confidence)}</p><p>${link(c.source_id)}<br>${esc(c.locator)}</p><p class="source-note">${esc(c.caveat)}</p></section>`;
      })
      .join(
        "",
      )}</div><div class="buttons"><button class="btn" id="answer-yes">Yes</button><button class="btn ghost" id="answer-no">No</button></div><div id="challenge-answer" aria-live="polite"></div><div class="buttons"><button class="btn ghost" id="next-question">Next question</button><button class="btn ghost" id="share-challenge">Copy challenge link</button><button class="btn ghost" id="challenge-card" disabled>Download explanation card</button></div><p class="source-note">Company self-reports; no independent remeasurement by ThirstyAI. Sources and caveats travel with the explanation.</p></article>`;
  }
  function bindChallenge() {
    const choose = (answer) => {
      revealed = true;
      const q = CHALLENGES[index];
      document.querySelector("#challenge-answer").innerHTML =
        `<div class="callout"><strong>${answer === q.answer ? "Correct." : "Look at the boundary."}</strong> ${q.explanation}</div>`;
      document.querySelector("#challenge-card").disabled = false;
    };
    document.querySelector("#answer-yes").onclick = () => choose(true);
    document.querySelector("#answer-no").onclick = () => choose(false);
    document.querySelector("#next-question").onclick = () => {
      index = (index + 1) % CHALLENGES.length;
      revealed = false;
      document.querySelector("main").innerHTML = challenge();
      bindChallenge();
    };
    document.querySelector("#share-challenge").onclick = async () => {
      const url = new URL(location.href);
      url.searchParams.delete("scenario");
      url.searchParams.set("question", CHALLENGES[index].id);
      url.hash = "challenge";
      try {
        await navigator.clipboard.writeText(url.href);
        toast("Challenge link copied");
      } catch {
        toast(
          "Clipboard unavailable. Open the source view to share the evidence.",
        );
      }
    };
    document.querySelector("#challenge-card").onclick = async () => {
      if (!revealed) return;
      const q = CHALLENGES[index];
      const sources = q.ids.map((id) =>
        data.companies.find((r) => r.observation_id === id),
      );
      const lines = [
        "SPOT THE MISSING BOUNDARY",
        q.question,
        q.explanation,
        ...sources.flatMap((c) => [
          `${c.company} ${c.metric}: ${c.value} ${c.unit}`,
          `${c.period} | ${c.scope}`,
          `${c.observation_id} | ${c.source_id} | ${c.locator}`,
        ]),
        "Company self-reports; not independently remeasured by ThirstyAI.",
        "Inspect original links and caveats in the challenge.",
        "ThirstyAI | purushotmanmooper96-bit.github.io/thirstyai/#challenge",
      ];
      try {
        await downloadTextCard(lines, "thirstyai-boundary-challenge.png");
        toast("Explanation card downloaded");
      } catch {
        toast("Card unavailable; inspect the source links above.");
      }
    };
  }
  const wanted = new URL(location.href).searchParams.get("question");
  const found = CHALLENGES.findIndex((q) => q.id === wanted);
  if (found >= 0) index = found;
  return { challenge, bindChallenge };
}
