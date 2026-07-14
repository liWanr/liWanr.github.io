(function () {
  "use strict";

  // 在这里填写需要忽略（不显示进度条）的固定页面路径
  // 支持结尾带或不带斜杠，会自动做归一化处理后精确匹配
  var IGNORED_PATHS = [
    "/essays/"
  ];

  var bar = null;
  var ticking = false;

  function normalizePath(path) {
    if (path.length > 1 && path.endsWith("/")) {
      path = path.slice(0, -1);
    }
    return path;
  }

  function isIgnoredPath() {
    var current = normalizePath(window.location.pathname);
    return IGNORED_PATHS.some(function (p) {
      return normalizePath(p) === current;
    });
  }

  function createBar() {
    bar = document.createElement("div");
    bar.className = "scroll-progress-bar";
    document.body.appendChild(bar);
  }

  function updateProgress() {
    ticking = false;

    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    var scrollHeight = document.documentElement.scrollHeight;
    var clientHeight = document.documentElement.clientHeight;
    var scrollable = scrollHeight - clientHeight;

    if (scrollable <= 0) {
      // 页面本身没有滚动条，一屏能显示完，隐藏进度条
      bar.style.opacity = "0";
      bar.style.width = "0%";
      return;
    }

    var progress = scrollTop / scrollable;
    progress = Math.min(1, Math.max(0, progress));

    bar.style.opacity = "1";
    bar.style.width = (progress * 100) + "%";
  }

  function onScrollOrResize() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(updateProgress);
    }
  }

  function init() {
    if (isIgnoredPath()) {
      return;
    }
    createBar();
    updateProgress();
    window.addEventListener("scroll", onScrollOrResize, { passive: true });
    window.addEventListener("resize", onScrollOrResize);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();