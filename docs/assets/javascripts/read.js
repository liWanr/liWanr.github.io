(() => {
  const titleSelector = '.feature-table tbody td:not(:first-child), .feature-table tbody td:first-child small';

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

  // 尺寸调整时更新文本溢出提示（顶栏计算已交由全局 JS 接管）
  addEventListener('resize', updateTitles);

  ['load', 'DOMContentLoaded'].forEach(ev => addEventListener(ev, build));
  window.document$?.subscribe(build);

  if (document.readyState !== 'loading') build();
})();