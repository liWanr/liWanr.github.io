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
      if (li && !li.querySelector(".explore-title")) {
        const a = img.closest("a") || li;
        
        // 1. 克隆 a 标签用于安全提取标题内容
        const clone = a.cloneNode(true);
        clone.querySelectorAll("img").forEach(i => i.remove());
        
        const titleText = clone.textContent.trim();
        const finalTitle = titleText || img.alt.trim();

        if (finalTitle) {
          // 2. 创建标题段落
          const p = document.createElement("p");
          p.className = "explore-title";
          
          if (titleText) {
            while (clone.firstChild) {
              p.appendChild(clone.firstChild);
            }
          } else {
            p.textContent = finalTitle;
          }

          // 3. 【核心修复】将 <a> 里的所有节点清空，只重新挂载 <img>，确保 <a> 恢复纯净
          if (a.tagName === "A") {
            a.replaceChildren(img); // 仅保留 img，消灭任何文本行高带来的高度挤压
          }

          // 4. 把标题放入 li 底部
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