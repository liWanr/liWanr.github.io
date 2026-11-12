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

  /* 2.2 返回顶部按钮：滚动时唤醒显示，停止滚动 1 秒后平滑淡出 */
  const initBackToTop = () => {
    if (window._backToTopInitialized) return;
    window._backToTopInitialized = true;

    // 动态注入平滑过渡的 CSS 样式
    const styleEl = document.createElement('style');
    styleEl.innerHTML = `
      button[data-md-component="top"] {
        transition: opacity 0.4s ease, visibility 0.4s ease !important;
      }
    `;
    document.head.append(styleEl);

    let hideTimer = null;

    window.addEventListener('scroll', () => {
      const btn = document.querySelector('button[data-md-component="top"]');
      if (!btn) return;

      // 只要发生滚动，立刻清除隐藏状态，使按钮恢复显示
      btn.style.opacity = '';
      btn.style.visibility = '';

      clearTimeout(hideTimer);
      
      // 停止滚动 1 秒后，开始平滑淡出
      hideTimer = setTimeout(() => {
        btn.style.opacity = '0';
        btn.style.visibility = 'hidden';
      }, 1500);
    }, { passive: true });
  };

  const initAll = () => {
    bar.isConnected || document.body.append(bar);
    updateBar();
    mergeCells();
    initBackToTop();
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