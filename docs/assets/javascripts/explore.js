(() => {
  if (window.__exploreBound) return;
  window.__exploreBound = true;

  const STEP = 200;  // 同一行相邻两张卡片的错开时间（ms）
  const JITTER = 40; // 额外随机抖动（ms）
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches || !window.IntersectionObserver;
  const queue = new Set();
  let timer;

  const el = (tag, props, ...kids) => {
    const e = Object.assign(document.createElement(tag), props);
    e.append(...kids.filter(Boolean));
    return e;
  };

  const shuffle = a => {
    for (let i = a.length; --i;) {
      const j = Math.random() * (i + 1) | 0;
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };

  // 同一批准备好的卡片：按行分组，行内随机排序，依次错开出现
  const flush = () => {
    timer = 0;
    const rows = {};
    queue.forEach(c => c._in && (rows[c.offsetTop] ||= []).push(c));
    queue.clear();
    Object.values(rows).forEach(row => shuffle(row).forEach((c, i) => {
      c.style.transitionDelay = `${i * STEP + Math.random() * JITTER}ms`;
      c.className = "explore-visible";
    }));
  };

  const io = still ? null : new IntersectionObserver(entries => entries.forEach(async ({ target: c, isIntersecting }) => {
    c._in = isIntersecting;

    // 离开视窗：重置，下次进入再播放动画
    if (!isIntersecting) {
      queue.delete(c);
      c.style.transitionDelay = "";
      c.className = "explore-pending";
      return;
    }

    // 进入视窗：强制立即加载并提高优先级，加载解码完再出现
    const imgs = [...c.querySelectorAll("img")];
    imgs.forEach(i => (i.loading = "eager", i.fetchPriority = "high"));
    await Promise.all(imgs.map(i => i.decode?.().catch(() => {})));
    if (!c._in) return;

    queue.add(c);
    timer ||= setTimeout(() => requestAnimationFrame(flush), 30);
  }), { threshold: .1 });

  // 从 JSON 生成卡片（每个容器只请求一次）
  const setup = box => (box._p ||= (async () => {
    let data;
    try {
      data = await (await fetch(box.dataset.json)).json();
    } catch (e) {
      return console.error("explore: 读取 JSON 失败", box.dataset.json, e);
    }

    box.replaceChildren(el("ul", null, ...data.map(({ title, sub, img, link }) => {
      const li = el("li", { className: still ? "explore-visible" : "explore-pending" },
        el(link ? "a" : "p", link && { href: link, target: "_blank", rel: "noopener" },
          el("img", { loading: "lazy", decoding: "async", alt: [title, sub].filter(Boolean).join(" "), src: img })),
        el("p", { className: "explore-title" }, title, sub && el("small", null, " ", sub)));
      io?.observe(li);
      return li;
    })));
  })());

  const init = async () => {
    await Promise.all([...document.querySelectorAll(".explore[data-json]")].map(setup));
    const n = document.getElementById("album-count");
    if (n) n.textContent = document.querySelectorAll(".explore li").length;
  };

  document.readyState === "loading" ? addEventListener("DOMContentLoaded", init, { once: true }) : init();
  window.document$?.subscribe(init);
})();