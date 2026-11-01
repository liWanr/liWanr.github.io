(() => {
  const root = document.documentElement;
  const IGNORED = ['/essays'];
  const bar = Object.assign(document.createElement('div'), { className: 'scroll-progress-bar' });
  let barTicking = false, headerOffset = 0, headerUntil = 0, headerRunning = false;

  /* 1. 滚动进度条 */
  const updateBar = () => {
    barTicking = false;
    const { scrollTop, scrollHeight, clientHeight } = root;
    const max = scrollHeight - clientHeight;
    bar.style.display = IGNORED.includes(location.pathname.replace(/\/$/, '')) ? 'none' : '';
    bar.style.opacity = +(max > 0);
    bar.style.width = (max > 0 ? Math.min(1, Math.max(0, scrollTop / max)) * 100 : 0) + '%';
  };

  /* 2. 顶栏偏移（动画期间持续测量 600ms） */
  const measureHeader = () => {
    const offset = Math.round(Math.max(0, ...[...document.querySelectorAll('.md-header, .md-tabs')]
      .filter(el => /sticky|fixed/.test(getComputedStyle(el).position))
      .map(el => el.getBoundingClientRect().bottom)));
    if (offset !== headerOffset) root.style.setProperty('--ft-site-header', `${headerOffset = offset}px`);
  };

  const tick = () => {
    measureHeader();
    (headerRunning = performance.now() < headerUntil) && requestAnimationFrame(tick);
  };

  const onChange = () => {
    if (!barTicking) { barTicking = true; requestAnimationFrame(updateBar); }
    headerUntil = performance.now() + 600;
    if (!headerRunning) { headerRunning = true; requestAnimationFrame(tick); }
  };

  /* 2.1 合并单元格（仅 .sanguo 表格）：<< 并入左侧，>> 并入右侧 */
  const mergeCells = () => {
    document.querySelectorAll('.sanguo table:not([data-merged])').forEach(table => {
      table.dataset.merged = 1;
      table.querySelectorAll('tr').forEach(tr => {
        let anchor;
        [...tr.children].forEach(c => {
          if (anchor && c.textContent.trim() === '<<') { anchor.colSpan += c.colSpan; c.remove(); }
          else anchor = c;
        });
        [...tr.children].forEach(c => {
          const next = c.nextElementSibling;
          if (next && c.textContent.trim() === '>>') { next.colSpan += c.colSpan; c.remove(); }
        });
      });
    });
  };

  const initAll = () => {
    bar.isConnected || document.body.append(bar);
    updateBar();
    mergeCells();
    document.querySelectorAll('.md-typeset table thead th[align]').forEach(th => th.style.textAlign = th.align);
    onChange();
  };

  /* 3. 事件绑定 */
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="http"]');
    if (a && a.origin !== location.origin && !a.classList.contains('glightbox')) {
      e.preventDefault();
      open(a.href, '_blank', 'noopener,noreferrer');
    }
  });

  addEventListener('scroll', onChange, { passive: true });
  addEventListener('resize', onChange);
  addEventListener('load', onChange);

  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', initAll) : initAll();
  window.document$?.subscribe?.(initAll);
})();