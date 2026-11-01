(() => {
  // 状态图标：todo 未读 / reading 在读 / done 已读
  const I = {
    todo: '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6m0-6 6 6"/>',
    reading: '<path d="M12 2v4M16.2 7.8l2.9-2.9M18 12h4M16.2 16.2l2.9 2.9M12 18v4M4.9 19.1l2.9-2.9M2 12h4M4.9 4.9l2.9 2.9"/>',
    done: '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'
  };

  const render = async box => {
    if (box.dataset.ok) return;
    box.dataset.ok = 1;
    try {
      const j = await (await fetch(box.dataset.src)).json();
      box.innerHTML = '<div class=ft-head><span>书名</span><span>作者</span><span>状态</span></div>' +
        Object.entries(j).map(([c, l]) =>
          `<table class=c><thead><tr><th>${c}<th><th></thead>` +
          l.map(({ title, sub, author, status, link }) => {
            const g = `<svg viewBox="0 0 24 24">${I[status]}</svg>`;
            return `<tr class=${status}><td><strong>${title}</strong><small>${sub}</small><td><em>${author}</em><td>${link ? `<a href="${link}">${g}</a>` : g}`;
          }).join('') + '</table>').join('');
      box.querySelectorAll('em').forEach(e => e.title = e.textContent);
      const n = document.getElementById('book-count');
      if (n) n.textContent = Object.values(j).flat().length;
    } catch { box.textContent = '书单加载失败'; }
  };

  const go = () => document.querySelectorAll('.books-table[data-src]').forEach(render);
  window.document$?.subscribe(go);
  document.readyState == 'loading' ? addEventListener('DOMContentLoaded', go) : go();
})();