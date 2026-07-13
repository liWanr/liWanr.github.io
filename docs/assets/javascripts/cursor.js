(function () {
  if (!matchMedia("(pointer: fine)").matches) return;

  var cursor = document.createElement("div");
  cursor.id = "cursor";
  document.body.appendChild(cursor);

  var toggleBtn = document.createElement("button");
  toggleBtn.id = "cursor-toggle";
  toggleBtn.title = "切换鼠标特效";
  toggleBtn.textContent = "●";
  document.body.appendChild(toggleBtn);

  var targetX = 0, targetY = 0;
  var currentX = 0, currentY = 0;
  var scale = 1;
  var isCursorEnabled = true;
  var hasPositioned = false; // 关键：标记是否已经拿到过第一次真实坐标

  var HALF_OF_CURSOR = 6;
  var LERP_FACTOR = 0.1;

  function updateCursor() {
    if (isCursorEnabled && hasPositioned) {
      currentX += (targetX - currentX) * LERP_FACTOR;
      currentY += (targetY - currentY) * LERP_FACTOR;
      cursor.style.transform =
        "translate3d(" + currentX + "px, " + currentY + "px, 0) scale(" + scale + ")";
    }
    requestAnimationFrame(updateCursor);
  }

  function getCursorPreference() {
    try {
      return localStorage.getItem("cursor-disabled") !== "true";
    } catch (e) {
      return true;
    }
  }

  function setCursorPreference(enabled) {
    try {
      localStorage.setItem("cursor-disabled", enabled ? "false" : "true");
    } catch (e) {}
  }

  function updateIconState() {
    toggleBtn.classList.toggle("opacity-50", !isCursorEnabled);
  }

  isCursorEnabled = getCursorPreference();
  updateIconState();
  document.documentElement.classList.toggle("has-custom-cursor", isCursorEnabled);

  toggleBtn.addEventListener("click", function () {
    isCursorEnabled = !isCursorEnabled;
    setCursorPreference(isCursorEnabled);
    updateIconState();
    document.documentElement.classList.toggle("has-custom-cursor", isCursorEnabled);
    if (!isCursorEnabled) cursor.style.opacity = "0";
  });

  window.addEventListener("mousemove", function (e) {
    if (!isCursorEnabled) return;
    targetX = e.clientX - HALF_OF_CURSOR;
    targetY = e.clientY - HALF_OF_CURSOR;

    if (!hasPositioned) {
      // 第一次拿到坐标：直接原地摆好，不做缓动滑动
      currentX = targetX;
      currentY = targetY;
      cursor.style.transform =
        "translate3d(" + currentX + "px, " + currentY + "px, 0) scale(" + scale + ")";
      hasPositioned = true;
    }

    if (cursor.style.opacity !== "1") cursor.style.opacity = "1";
  });

  document.addEventListener("mouseover", function (e) {
    if (!isCursorEnabled) return;
    scale = e.target.closest && e.target.closest("a, button") ? 1.8 : 1;
  });

  updateCursor();
})();