(() => {
  if (window.__exploreBound) return;
  window.__exploreBound = true;

  const init = () => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hasObserver = "IntersectionObserver" in window;

    // 1. 统一处理图片属性与标题补全
    document.querySelectorAll(".explore img").forEach(img => {
      if (!img.hasAttribute("loading")) img.loading = "lazy";
      img.decoding = "async";

      const li = img.closest("li");
      if (li && img.alt && !li.querySelector(".explore-title")) {
        const titleText = img.alt.trim();
        if (titleText) {
          const p = document.createElement("p");
          p.className = "explore-title";
          p.textContent = titleText;
          li.appendChild(p);
        }
      }
    });

    if (reduceMotion || !hasObserver) {
      document.querySelectorAll(".explore ul > li").forEach(c => c.classList.add("explore-visible"));
      return;
    }

    // 2. 交叉观察器：卡片露出 1/3 时触发
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const card = entry.target;
        obs.unobserve(card);

        // 利用 Promise.all 并发等待所有图片解码完成，代码瞬间清爽
        const imgs = [...card.querySelectorAll("img")];
        Promise.all(imgs.map(img => (typeof img.decode === "function" ? img.decode().catch(() => {}) : Promise.resolve())))
          .then(() => {
            requestAnimationFrame(() => {
              card.classList.remove("explore-pending");
              card.classList.add("explore-visible");
            });
          });
      });
    }, { threshold: 0.1 });

    // 3. 初始化卡片状态
    document.querySelectorAll(".explore ul > li").forEach(card => {
      if (card.dataset.exploreRevealReady) return;
      card.dataset.exploreRevealReady = "true";
      card.classList.add("explore-pending");
      observer.observe(card);
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }

  window.addEventListener("load", init);
  window.document$?.subscribe?.(init);
})();