const supported = ["en", "zh", "ja", "ko"];
const aliases = { "zh-cn": "zh", "zh-sg": "zh", "ja-jp": "ja", "ko-kr": "ko" };
const nodeDetailKeys = {
  intent: "intentDetail",
  harness: "harnessDetail",
  graph: "graphDetail",
  loop: "loopDetail",
  evidence: "evidenceDetail",
};

let messages = {};

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
  messages = await response.json();

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = messages[node.dataset.i18n];
    if (typeof value === "string") node.textContent = value;
  });

  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    const value = messages[node.dataset.i18nPlaceholder];
    if (typeof value === "string") {
      node.value = value;
      node.placeholder = value;
      updateCharacterCount(node);
    }
  });

  document.documentElement.lang = language === "zh" ? "zh-CN" : language;
  document.title = messages.pageTitle;
  localStorage.setItem("hgl-language", language);

  document.querySelectorAll("[data-lang]").forEach((button) => {
    const active = button.dataset.lang === language;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  const activeNode = document.querySelector(".blueprint-node.active");
  if (activeNode) updateNodeDetail(activeNode.dataset.node);

  if (updateUrl) {
    const url = new URL(window.location.href);
    url.searchParams.set("lang", language);
    history.replaceState({}, "", url);
  }
}

function updateNodeDetail(nodeName) {
  const detail = document.querySelector("[data-node-detail]");
  const key = nodeDetailKeys[nodeName];
  if (detail && key && messages[key]) detail.textContent = messages[key];
}

function showToast() {
  const toast = document.querySelector(".toast");
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 1800);
}

async function copyPrompt(targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;
  const value = "value" in target ? target.value : target.textContent;
  await navigator.clipboard.writeText(value.trim());
  showToast();
}

function updateCharacterCount(input) {
  const count = input.closest(".prompt-box")?.querySelector(".character-count b");
  if (count) count.textContent = String(input.value.length);
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});

document.querySelectorAll("[data-copy-target]").forEach((button) => {
  button.addEventListener("click", () => copyPrompt(button.dataset.copyTarget));
});

document.querySelectorAll("[data-i18n-placeholder]").forEach((input) => {
  input.addEventListener("input", () => updateCharacterCount(input));
  updateCharacterCount(input);
});

document.querySelectorAll("nav a[href^='#']").forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelectorAll("nav a").forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
  });
});

document.querySelectorAll(".blueprint-node").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".blueprint-node").forEach((node) => node.classList.remove("active"));
    button.classList.add("active");
    updateNodeDetail(button.dataset.node);
  });
});

setLanguage(preferredLanguage(), false).catch(() => setLanguage("en"));
