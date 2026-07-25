const supported = ["en", "zh", "ja", "ko"];
const aliases = { "zh-cn": "zh", "zh-sg": "zh", "ja-jp": "ja", "ko-kr": "ko" };

function preferredLanguage() {
  const query = new URLSearchParams(window.location.search).get("lang");
  if (supported.includes(query)) return query;
  const stored = localStorage.getItem("hgl-language");
  if (supported.includes(stored)) return stored;
  const browser = navigator.language.toLowerCase();
  return aliases[browser] || supported.find((code) => browser.startsWith(code)) || "en";
}

async function setLanguage(language, updateUrl = true) {
  if (!supported.includes(language)) language = "en";
  const response = await fetch(`i18n/${language}.json`);
  if (!response.ok) throw new Error(`Unable to load ${language}`);
  const messages = await response.json();
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = messages[node.dataset.i18n];
    if (typeof value === "string") node.textContent = value;
  });
  document.documentElement.lang = language === "zh" ? "zh-CN" : language;
  document.title = messages.pageTitle;
  localStorage.setItem("hgl-language", language);
  document.querySelectorAll("[data-lang]").forEach((button) => {
    const active = button.dataset.lang === language;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  if (updateUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set("lang", language);
    history.replaceState({}, "", url);
  }
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});
setLanguage(preferredLanguage(), false).catch(() => setLanguage("en"));

const canvas = document.getElementById("signal-field");
const context = canvas.getContext("2d");
let width = 0;
let height = 0;
let nodes = [];

function resize() {
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  width = window.innerWidth;
  height = window.innerHeight;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;
  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  nodes = Array.from({ length: Math.max(12, Math.floor(width / 90)) }, (_, index) => ({
    x: (index * 173) % width,
    y: (index * 97 + 80) % height,
    phase: index * 0.71,
  }));
}

function draw(time) {
  context.clearRect(0, 0, width, height);
  context.lineWidth = 0.7;
  nodes.forEach((node, index) => {
    const x = node.x + Math.sin(time * 0.00018 + node.phase) * 22;
    const y = node.y + Math.cos(time * 0.00014 + node.phase) * 18;
    const next = nodes[(index + 3) % nodes.length];
    const nx = next.x + Math.sin(time * 0.00018 + next.phase) * 22;
    const ny = next.y + Math.cos(time * 0.00014 + next.phase) * 18;
    context.beginPath();
    context.moveTo(x, y);
    context.lineTo(nx, ny);
    context.strokeStyle = "rgba(83,246,199,.12)";
    context.stroke();
    context.beginPath();
    context.arc(x, y, index % 4 === 0 ? 2.4 : 1.4, 0, Math.PI * 2);
    context.fillStyle = index % 4 === 0 ? "rgba(216,243,107,.8)" : "rgba(83,246,199,.55)";
    context.fill();
  });
  requestAnimationFrame(draw);
}

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  window.addEventListener("resize", resize);
  resize();
  requestAnimationFrame(draw);
}

