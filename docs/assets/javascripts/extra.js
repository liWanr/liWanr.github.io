(() => {
  /* ==================== 1. 滚动进度条逻辑 ==================== */
  const IGNORED = ['/essays/'];
  const norm = p => p.replace(/\/$/, '');
  const isIgnored = IGNORED.some(p => norm(p) === norm(location.pathname));

  let bar = null;
  if (!isIgnored) {
    bar = document.body.appendChild(document.createElement('div'));
    bar.className = 'scroll-progress-bar';
  }

  let barTicking = false;
  const updateBar = () => {
    barTicking = false;
    if (!bar) return;
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    const max = scrollHeight - clientHeight;
    const progress = max > 0 ? Math.min(1, Math.max(0, scrollTop / max)) : 0;

    bar.style.opacity = max > 0 ? '1' : '0';
    bar.style.width = `${progress * 100}%`;
  };

  const triggerBar = () => {
    if (!barTicking && bar) {
      barTicking = true;
      requestAnimationFrame(updateBar);
    }
  };

  /* ==================== 2. 表格吸顶与顶栏偏移逻辑 ==================== */
  let lastHeaderOffset = 0, headerUntil = 0, headerRunning = false;

  const measureHeader = () => {
    let offset = 0;
    document.querySelectorAll('.md-header, .md-tabs').forEach(el => {
      if (/sticky|fixed/.test(getComputedStyle(el).position)) {
        offset = Math.max(offset, el.getBoundingClientRect().bottom);
      }
    });
    if ((offset = Math.max(0, Math.round(offset))) !== lastHeaderOffset) {
      document.documentElement.style.setProperty('--ft-site-header', `${lastHeaderOffset = offset}px`);
    }
  };

  const kickHeader = () => {
    headerUntil = performance.now() + 600;
    if (!headerRunning && (headerRunning = true)) {
      requestAnimationFrame(function tick() {
        measureHeader();
        performance.now() < headerUntil ? requestAnimationFrame(tick) : headerRunning = false;
      });
    }
  };

  const buildTables = () => {
    document.querySelectorAll('.md-typeset table thead th').forEach(th => {
      const align = th.getAttribute('align') || (th.style.textAlign || '').match(/left|center|right/i)?.[0];
      if (align) th.style.textAlign = align;
    });
    kickHeader();
  };

  /* ==================== 3. 统一初始化与事件绑定 ==================== */
  // A. 外链安全拦截
  document.addEventListener('click', e => {
    const link = e.target.closest('a[href^="http"]');
    if (link && !link.href.startsWith(location.origin) && !link.classList.contains('glightbox')) {
      e.preventDefault();
      window.open(link.href, '_blank', 'noopener,noreferrer');
    }
  });

  // B. 页面滚动与尺寸调整事件（合并监听器）
  addEventListener('scroll', () => {
    triggerBar();
    kickHeader();
  }, { passive: true });

  addEventListener('resize', () => {
    triggerBar();
    kickHeader();
  });

  // C. 页面加载与 Material 主题 DOM$ 监听
  const initAll = () => {
    updateBar();
    buildTables();
  };

  ['load', 'DOMContentLoaded'].forEach(ev => addEventListener(ev, initAll));
  window.document$?.subscribe?.(initAll);

  if (document.readyState !== 'loading') initAll();
})();