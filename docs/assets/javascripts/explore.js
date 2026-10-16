(() => {
  if (window.__exploreBound) return;
  window.__exploreBound = true;

  const init = () => {
    const countEl = document.getElementById("album-count");
    if (countEl) {
      countEl.textContent = document.querySelectorAll(".explore li").length;
    }

    // 1. 统一处理图片属性与标题补全
    document.querySelectorAll(".explore img").forEach(img => {
      img.loading ||= "lazy";
      img.decoding = "async";

      const li = img.closest("li");
      if (!li || li.querySelector(".explore-title")) return;

      const a = img.closest("a") || li;
      const clone = a.cloneNode(true);
      clone.querySelectorAll("img").forEach(i => i.remove());

      const titleText = clone.textContent.trim();
      const finalTitle = titleText || img.alt.trim();
      if (!finalTitle) return;

      const p = document.createElement("p");
      p.className = "explore-title";
      if (titleText) {
        p.replaceChildren(...clone.childNodes);
      } else {
        p.textContent = finalTitle;
      }

      if (a.tagName === "A") a.replaceChildren(img);
      li.appendChild(p);
    });

    const cards = document.querySelectorAll(".explore ul > li");
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || !("IntersectionObserver" in window)) {
      cards.forEach(c => c.classList.add("explore-visible"));
      return;
    }

    // 2. 交叉观察器
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(async entry => {
        if (!entry.isIntersecting) return;
        obs.unobserve(entry.target);

        await Promise.all([...entry.target.querySelectorAll("img")].map(img => img.decode?.().catch(() => {})));
        
        requestAnimationFrame(() => {
          entry.target.classList.remove("explore-pending");
          entry.target.classList.add("explore-visible");
        });
      });
    }, { threshold: 0.1 });

    // 3. 初始化卡片状态
    cards.forEach(card => {
      if (card.dataset.exploreReady) return;
      card.dataset.exploreReady = "true";
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