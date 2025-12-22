// Simple i18n helper (no framework)
(function () {
  const STORAGE_KEY = "lang";
  const DEFAULT_LANG = "zh";

  const dict = {
    zh: {
      "common.leaderboard": "排行榜",
      "common.admin": "后台",
      "common.settings": "设置",
      "common.login": "登录",
      "common.logout": "退出登录",
      "common.home": "首页",
      "common.cancel": "取消",
      "common.startGame": "开始游戏",
      "common.loading": "加载中...",
      "common.networkError": "网络异常",
      "common.notAdmin": "你不是管理员，无法进入后台",
      "common.puzzle": "题目",
      "common.playNow": "开始推理 ->",
      "common.failedToLoad": "加载失败",
      "common.noData": "暂无数据",
      "index.subtitle": "海龟汤推理小游戏",
      "index.fetching": "正在获取题目...",
      "play_mode.title": "模式选择",
      "play_mode.gameMode": "游戏模式",
      "play_mode.storyMode": "故事模式",
      "play_mode.storyDesc": "轻松推理，不限时。",
      "play_mode.timeAttack": "计时模式",
      "play_mode.timeDesc": "5分钟内完成推理！",
      "play_mode.detective": "挑战模式",
      "play_mode.detectiveDesc": "资源有限：20个问题。",
      "play.titleFallback": "推理对局",
      "play.situation": "情境",
      "play.solved": "已解开",
      "play.giveUp": "放弃",
      "play.askPlaceholder": "请输入一个是/否问题...",
      "play.time": "时间",
      "play.questions": "提问",
      "play.left": "剩余",
      "play.you": "你",
      "play.answer": "回答",
      "play.system": "系统",
      "play.result": "结果",
      "play.timeOver": "时间到。",
      "play.loginAgain": "请重新登录。",
      "play.missingSession": "缺少会话信息",
      "play.finished": "结算",
      "play.score": "得分",
      "play.success": "成功",
      "play.fail": "失败",
      "play.case": "案件",
      "play.situationLabel": "情境",
      "play.askHint": "请通过“是/否”问题推理出真相！",
      "play.modeLabel": "模式",
      "play_mode.missingPuzzleId": "缺少题目 ID",
      "play_mode.pleaseLogin": "请先登录",
      "scoreboard.title": "排行榜",
      "scoreboard.subtitle": "看看谁是最强侦探",
      "scoreboard.rank": "排名",
      "scoreboard.player": "玩家",
      "scoreboard.totalScore": "总分",
      "scoreboard.noScores": "暂无得分",
      "auth.welcomeBack": "欢迎回来",
      "auth.signInToPlay": "登录后开始游戏",
      "auth.joinUs": "加入我们",
      "auth.createAccount": "注册账号开始游戏",
      "auth.username": "用户名",
      "auth.password": "密码",
      "auth.login": "登录",
      "auth.register": "注册",
      "auth.noAccount": "没有账号？去注册",
      "auth.haveAccount": "已有账号？去登录",
      "settings.title": "设置",
      "settings.subtitle": "个性化你的体验",
      "settings.language": "语言",
      "settings.zh": "中文",
      "settings.en": "English",
      "settings.save": "保存",
      "settings.back": "返回",
    },
    en: {
      "common.leaderboard": "Leaderboard",
      "common.admin": "Admin",
      "common.settings": "Settings",
      "common.login": "Login",
      "common.logout": "Logout",
      "common.home": "Home",
      "common.cancel": "Cancel",
      "common.startGame": "Start Game",
      "common.loading": "Loading...",
      "common.networkError": "Network error",
      "common.notAdmin": "You are not an admin and cannot access the console",
      "common.puzzle": "PUZZLE",
      "common.playNow": "Play Now ->",
      "common.failedToLoad": "Failed to load",
      "common.noData": "No data",
      "index.subtitle": "Lateral Thinking Mystery Game",
      "index.fetching": "Fetching puzzles...",
      "play_mode.title": "Mission Setup",
      "play_mode.gameMode": "Game Mode",
      "play_mode.storyMode": "Story Mode",
      "play_mode.storyDesc": "Relax and solve at your own pace.",
      "play_mode.timeAttack": "Time Attack",
      "play_mode.timeDesc": "Solve within 5 minutes!",
      "play_mode.detective": "Detective",
      "play_mode.detectiveDesc": "Limited resources: 20 questions.",
      "play.titleFallback": "Turtle Soup Play",
      "play.situation": "THE SITUATION",
      "play.solved": "Solved",
      "play.giveUp": "Give Up",
      "play.askPlaceholder": "Ask a Yes/No question...",
      "play.time": "Time",
      "play.questions": "Questions",
      "play.left": "left",
      "play.you": "You",
      "play.answer": "Answer",
      "play.system": "System",
      "play.result": "Result",
      "play.timeOver": "Time is over.",
      "play.loginAgain": "Please login again.",
      "play.missingSession": "Missing session",
      "play.finished": "Finished",
      "play.score": "score",
      "play.success": "success",
      "play.fail": "fail",
      "play.case": "Case",
      "play.situationLabel": "Situation",
      "play.askHint": "Ask Yes/No questions to find the truth!",
      "play.modeLabel": "MODE",
      "play_mode.missingPuzzleId": "Missing puzzle id",
      "play_mode.pleaseLogin": "Please login",
      "scoreboard.title": "Leaderboard",
      "scoreboard.subtitle": "Top detectives",
      "scoreboard.rank": "#",
      "scoreboard.player": "Player",
      "scoreboard.totalScore": "Total Score",
      "scoreboard.noScores": "No scores yet.",
      "auth.welcomeBack": "Welcome back",
      "auth.signInToPlay": "Sign in to play",
      "auth.joinUs": "Join us",
      "auth.createAccount": "Create an account to play",
      "auth.username": "Username",
      "auth.password": "Password",
      "auth.login": "Login",
      "auth.register": "Register",
      "auth.noAccount": "No account? Register",
      "auth.haveAccount": "Already have an account? Login",
      "settings.title": "Settings",
      "settings.subtitle": "Personalize your experience",
      "settings.language": "Language",
      "settings.zh": "中文",
      "settings.en": "English",
      "settings.save": "Save",
      "settings.back": "Back",
    },
  };

  function getLang() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_LANG;
  }

  function setLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang);
  }

  function t(key, fallback) {
    const lang = getLang();
    return (dict[lang] && dict[lang][key]) || fallback || key;
  }

  function applyTranslations(root) {
    const container = root || document;
    container.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      el.textContent = t(key, el.textContent);
    });
    container.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
      const key = el.getAttribute("data-i18n-placeholder");
      el.setAttribute("placeholder", t(key, el.getAttribute("placeholder")));
    });
    document.documentElement.setAttribute("lang", getLang());
  }

  window.I18N = { getLang, setLang, t, applyTranslations };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => applyTranslations());
  } else {
    applyTranslations();
  }
})();
