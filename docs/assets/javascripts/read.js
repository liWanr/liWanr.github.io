(() => {
  let last = -1, until = 0, running = false;
  const titleSelector = '.feature-table tbody td:not(:first-child), .feature-table tbody td:first-child small';

  const measure = () => {
    let offset = 0;
    document.querySelectorAll('.md-header, .md-tabs').forEach(el => {
      if (['sticky', 'fixed'].includes(getComputedStyle(el).position)) {
        offset = Math.max(offset, el.getBoundingClientRect().bottom);
      }
    });

    offset = Math.max(0, Math.round(offset));
    if (offset !== last) {
      last = offset;
      document.documentElement.style.setProperty('--ft-site-header', `${offset}px`);
    }
  };

  const kick = () => {
    until = performance.now() + 600;
    if (running) return;
    running = true;

    const tick = () => {
      measure();
      if (performance.now() < until) requestAnimationFrame(tick);
      else running = false;
    };
    requestAnimationFrame(tick);
  };

  const updateTitles = () => {
    document.querySelectorAll(titleSelector).forEach(el => {
      const text = el.textContent.trim();
      if (text && el.scrollWidth > el.clientWidth + 1) el.setAttribute('title', text);
      else el.removeAttribute('title');
    });
  };

  const build = () => {
    document.querySelectorAll('.feature-table').forEach(box => {
      const header = box.querySelector('.ft-header');
      const source = box.querySelector('table:not(.ft-header) thead tr');
      if (!header || !source) return;

      header.querySelectorAll('th').forEach((th, i) => {
        const cell = source.cells[i];
        if (!cell) return;
        th.style.textAlign = cell.getAttribute('align') || 
          (cell.getAttribute('style') || '').match(/text-align\s*:\s*(left|center|right)/i)?.[1] || 
          'left';
      });
    });

    kick();
    updateTitles();
  };

  document.addEventListener('mouseover', e => {
    const el = e.target.closest?.(titleSelector);
    if (el) {
      const text = el.textContent.trim();
      if (text && el.scrollWidth > el.clientWidth + 1) el.setAttribute('title', text);
      else el.removeAttribute('title');
    }
  });

  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', () => { kick(); updateTitles(); });

  ['load', 'DOMContentLoaded'].forEach(ev => addEventListener(ev, build));
  window.document$?.subscribe(build);

  if (document.readyState !== 'loading') build();
  else kick();
})();