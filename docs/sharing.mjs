import { receiptLines } from "./scenario.mjs";
export async function downloadReceipt(b, a) {
  return downloadTextCard(receiptLines(b, a), "thirstyai-assumptions.png");
}
export async function downloadTextCard(lines, filename) {
  const canvas = document.createElement("canvas");
  canvas.width = 1400;
  const ctx = canvas.getContext("2d");
  const wrapped = [];
  lines.forEach((text, index) => {
    ctx.font = index === 0 ? "bold 34px sans-serif" : "24px sans-serif";
    const words = text.split(" ");
    let line = "";
    for (const word of words) {
      if (ctx.measureText(line + " " + word).width > 1250 && line) {
        wrapped.push({ text: line, index });
        line = word;
      } else line += (line ? " " : "") + word;
    }
    wrapped.push({ text: line, index });
  });
  canvas.height = Math.max(760, 110 + wrapped.length * 42);
  ctx.fillStyle = "#0c131b";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#8ce2da";
  ctx.lineWidth = 3;
  ctx.strokeRect(24, 24, 1352, canvas.height - 48);
  wrapped.forEach((line, i) => {
    ctx.font = line.index === 0 ? "bold 34px sans-serif" : "24px sans-serif";
    ctx.fillStyle =
      line.index === 1 ? "#f3cc86" : line.index === 0 ? "#8ce2da" : "#e8f0f2";
    ctx.fillText(line.text, 52, 75 + i * 42);
  });
  const blob = await new Promise((resolve) =>
    canvas.toBlob(resolve, "image/png"),
  );
  if (!blob) throw new Error("Image export unavailable");
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}
export function showEvidenceFallback(main, message) {
  const notice = document.createElement("div");
  notice.className = "callout warning";
  notice.setAttribute("role", "status");
  const text = document.createElement("p");
  text.textContent = `Interactive data unavailable. The published static evidence remains below. ${message}`;
  const retry = document.createElement("button");
  retry.className = "btn ghost";
  retry.textContent = "Retry interactive view";
  retry.onclick = () => location.reload();
  notice.append(text, retry);
  main.prepend(notice);
}
