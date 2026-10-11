(() => {
  const selectors = ['.md-header', '.md-tabs'];
  let last = -1, until = 0, running = false;

  function measure() {
    let offset = 0;

    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => {
        if (!['sticky', 'fixed'].includes(getComputedStyle(el).position)) return;
        const rect = el.getBoundingClientRect();
        if (rect.height > 0) offset = Math.max(offset, rect.bottom);
      });
    });

    offset = Math.max(0, Math.round(offset));

    if (offset !== last) {
      last = offset;
      document.documentElement.style.setProperty('--ft-site-header', offset + 'px');
    }
  }

  function kick() {
    until = performance.now() + 600;
    if (running) return;
    running = true;

    function tick() {
      measure();
      if (performance.now() < until) requestAnimationFrame(tick);
      else running = false;
    }

    requestAnimationFrame(tick);
  }

  function updateTitle(el) {
    if (!el) return;
    const text = el.textContent.trim();

    if (text && el.scrollWidth > el.clientWidth + 1) {
      el.setAttribute('title', text);
    } else {
      el.removeAttribute('title');
    }
  }

  function updateTitles() {
    document.querySelectorAll(
      '.feature-table tbody td:not(:first-child), ' +
      '.feature-table tbody td:first-child small'
    ).forEach(updateTitle);
  }

  function build() {
    document.querySelectorAll('.feature-table').forEach(box => {
      const header = box.querySelector('.ft-header');
      const source = box.querySelector('table:not(.ft-header) thead tr');

      if (!header || !source) return;

      header.querySelectorAll('th').forEach((th, i) => {
        const cell = source.cells[i];
        if (!cell) return;

        const style = cell.getAttribute('style') || '';
        const align = cell.getAttribute('align') ||
          style.match(/text-align\s*:\s*(left|center|right)/i)?.[1] ||
          'left';

        th.style.textAlign = align;
      });
    });

    kick();
    updateTitles();
  }

  document.addEventListener('mouseover', event => {
    const el = event.target.closest?.(
      '.feature-table tbody td:not(:first-child), ' +
      '.feature-table tbody td:first-child small'
    );
    if (el) updateTitle(el);
  });

  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', () => {
    kick();
    updateTitles();
  });

  addEventListener('load', build);
  document.addEventListener('DOMContentLoaded', build);
  if (window.document$) window.document$.subscribe(build);

  if (document.readyState !== 'loading') build();
  else kick();
})();