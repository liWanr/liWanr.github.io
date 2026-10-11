/* cover-wall.js:让分类标题的吸顶位置跟着站点顶部固定栏走。
   测量 .md-header 和(吸顶的).md-tabs 当前露出的底边,写入 --cw-site-header。
   顶栏自动隐藏、标签栏吸顶、窗口缩放都会自动跟随。 */
(function () {
  if (window.__cwBound) return;
  window.__cwBound = true;

  var SELECTORS = ['.md-header', '.md-tabs'];
  var last = -1, until = 0, running = false;

  function measure() {
    var off = 0;
    SELECTORS.forEach(function (s) {
      document.querySelectorAll(s).forEach(function (el) {
        var pos = getComputedStyle(el).position;
        if (pos !== 'sticky' && pos !== 'fixed') return;
        var r = el.getBoundingClientRect();
        if (r.height > 0) off = Math.max(off, r.bottom);
      });
    });
    off = Math.max(0, Math.round(off));
    if (off !== last) {
      last = off;
      document.documentElement.style.setProperty('--cw-site-header', off + 'px');
    }
  }
  function tick() {
    measure();
    if (performance.now() < until) requestAnimationFrame(tick);
    else running = false;
  }
  function kick() {
    until = performance.now() + 600;      /* 滚动/变化后逐帧跟随 600ms,之后停下 */
    if (!running) { running = true; requestAnimationFrame(tick); }
  }

  /* 祖先元素带 overflow:hidden/auto/scroll 会让 position:sticky 失效(比如外面套了内容标签页、卡片)。
     把它们改成 overflow:clip:同样裁剪内容,但不会变成滚动容器,吸顶就恢复了。
     真正在滚动的容器不动。 */
  function unblock() {
    document.querySelectorAll('.cover-wall').forEach(function (w) {
      for (var e = w.parentElement; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
        var s = getComputedStyle(e);
        if (!/(hidden|auto|scroll)/.test(s.overflowX + ' ' + s.overflowY)) continue;
        if (/(auto|scroll)/.test(s.overflowX + ' ' + s.overflowY) &&
            (e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1)) continue;
        e.style.overflow = 'clip';
      }
    });
  }
  function init() { unblock(); kick(); }

  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', kick);
  addEventListener('load', init);
  document.addEventListener('DOMContentLoaded', init);
  if (window.document$ && window.document$.subscribe) window.document$.subscribe(init); /* 即时导航换页 */
  if (document.readyState !== 'loading') init(); else kick();
})();