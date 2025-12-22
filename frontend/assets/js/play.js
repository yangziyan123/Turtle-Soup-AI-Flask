let sessionId = null;
let puzzleId = null;
let mode = null;
let limitSeconds = null;
let limitQuestions = null;
let startTime = null;
let questionUsed = 0;
let timerInterval = null;
let gameOver = false;

function t(key, fallback) {
  return window.I18N ? I18N.t(key, fallback) : fallback;
}

function getQueryParam(key) {
  const params = new URLSearchParams(window.location.search);
  return params.get(key);
}

function goBack() {
  history.back();
}

function addMessage(role, html) {
  const area = document.getElementById("chat-area");
  const div = document.createElement("div");
  div.className = "chat-msg " + role;
  div.innerHTML = html;
  area.appendChild(div);
  area.scrollTop = area.scrollHeight;
}

async function loadPuzzle() {
  const titleEl = document.getElementById("puzzle-title");
  const descEl = document.getElementById("puzzle-desc");
  const welcome = document.getElementById("welcome-msg");

  try {
    const lang = window.I18N && I18N.getLang ? I18N.getLang() : "zh";
    const res = await apiFetch(`/api/puzzles/${puzzleId}?lang=${encodeURIComponent(lang)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "puzzle_not_found");

    const title = data.title || t("play.titleFallback", "Mystery");
    const situation = data.description || "";

    titleEl.textContent = title;
    descEl.textContent = situation || " ";

    welcome.innerHTML =
      `${t("play.askHint", "Ask Yes/No questions to find the truth!")}` +
      `<br><br>` +
      `${t("play.case", "Case")}: <b>${title}</b><br>` +
      `${t("play.situationLabel", "Situation")}: "${situation}"`;
  } catch (err) {
    console.warn(err);
    titleEl.textContent = t("play.titleFallback", "Mystery");
    descEl.textContent = " ";
    welcome.textContent = t("play.askHint", "Ask Yes/No questions to find the truth!");
  }
}

function updateQuestionBox() {
  const box = document.getElementById("question-box");
  if (limitQuestions) {
    const remaining = Math.max(0, limitQuestions - questionUsed);
    box.textContent =
      `${t("play.questions", "Questions")}: ${questionUsed} / ${limitQuestions} ` +
      `(${t("play.left", "left")} ${remaining})`;
  } else {
    box.textContent = `${t("play.questions", "Questions")}: ${questionUsed}`;
  }
}

function startCountdown() {
  const box = document.getElementById("timer-box");
  if (!limitSeconds || !startTime) {
    box.textContent = `${t("play.time", "Time")}: --`;
    return;
  }

  function tick() {
    const now = Date.now();
    const elapsed = Math.floor((now - startTime) / 1000);
    const remaining = Math.max(0, limitSeconds - elapsed);
    const m = String(Math.floor(remaining / 60)).padStart(2, "0");
    const s = String(remaining % 60).padStart(2, "0");
    box.textContent = `${t("play.time", "Time")}: ${m}:${s}`;

    if (remaining <= 0 && timerInterval) {
      clearInterval(timerInterval);
      addMessage("system", `<b>${t("play.system", "System")}:</b> ${t("play.timeOver", "Time is over.")}`);
    }
  }

  tick();
  timerInterval = setInterval(tick, 1000);
}

async function sendQuestion() {
  const qInput = document.getElementById("question");
  const q = qInput.value.trim();
  if (!q) return;
  if (gameOver) return;
  if (!sessionId) {
    alert(t("play.missingSession", "Missing session"));
    return;
  }

  addMessage("user", `<b>${t("play.you", "You")}:</b> ${q}`);
  qInput.value = "";

  try {
    const res = await apiFetch("/api/play/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, question: q }),
    });
    const data = await res.json();

    if (res.status === 401) {
      addMessage("system", `<b>${t("play.system", "System")}:</b> ${t("play.loginAgain", "Please login again.")}`);
      window.location.href =
        `/login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
      return;
    }

    if (!res.ok) {
      addMessage("system", `<b>${t("play.system", "System")}:</b> ${data.error || "error"}`);
      return;
    }

    if (data.type === "game_over") {
      gameOver = true;
      if (timerInterval) clearInterval(timerInterval);
      addMessage("system", `<b>${t("play.result", "Result")}:</b> ${data.answer || ""}`);
      const statusText = document.getElementById("status-text");
      statusText.textContent = `${t("play.finished", "Finished")}: ${t("play.success", "success")}, ${t("play.score", "score")} ${data.score}`;
      const giveUpBtn = document.getElementById("give-up-btn");
      if (giveUpBtn) giveUpBtn.style.display = "none";
      const input = document.getElementById("question");
      if (input) input.disabled = true;
      return;
    }

    questionUsed += 1;
    updateQuestionBox();

    addMessage("ai", `<b>${t("play.answer", "Answer")}:</b> ${data.answer}`);
  } catch (err) {
    console.error(err);
    addMessage("system", `<b>${t("play.system", "System")}:</b> ${t("common.networkError", "Network error")}`);
  }
}

async function finishGame(result) {
  if (!sessionId) {
    alert(t("play.missingSession", "Missing session"));
    return;
  }
  if (gameOver) return;

  try {
    const res = await apiFetch("/api/play/finish", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, result }),
    });
    const data = await res.json();

    if (res.status === 401) {
      alert(t("play_mode.pleaseLogin", "Please login"));
      window.location.href =
        `/login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
      return;
    }

    const statusText = document.getElementById("status-text");
    if (!res.ok) {
      statusText.textContent = data.error || "finish failed";
      return;
    }

    gameOver = true;
    if (timerInterval) clearInterval(timerInterval);

    const resultText = t("play.fail", "fail");
    statusText.textContent = `${t("play.finished", "Finished")}: ${resultText}, ${t("play.score", "score")} ${data.score}`;
    const input = document.getElementById("question");
    if (input) input.disabled = true;
  } catch (err) {
    console.error(err);
    alert(t("common.networkError", "Network error"));
  }
}

function init() {
  sessionId = getQueryParam("session_id");
  puzzleId = getQueryParam("puzzle_id");
  mode = getQueryParam("mode");

  limitSeconds = parseInt(getQueryParam("limit_seconds"), 10);
  limitSeconds = Number.isFinite(limitSeconds) ? limitSeconds : null;

  limitQuestions = parseInt(getQueryParam("limit_questions"), 10);
  limitQuestions = Number.isFinite(limitQuestions) ? limitQuestions : null;

  const startTimeStr = getQueryParam("start_time");
  startTime = startTimeStr ? Date.parse(startTimeStr) : null;

  if (mode === "timed" && !limitSeconds) limitSeconds = 300;
  if (mode === "timed" && !startTime) startTime = Date.now();

  const modeEl = document.getElementById("mode-text");
  if (mode) modeEl.textContent = `${t("play.modeLabel", "MODE")}: ${mode.toUpperCase()}`;

  updateQuestionBox();
  startCountdown();
  loadPuzzle();

  const input = document.getElementById("question");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
      }
    });
  }
}

window.sendQuestion = sendQuestion;
window.finishGame = finishGame;
window.goBack = goBack;

window.addEventListener("DOMContentLoaded", init);
