(() => {
  if (window.__exploreBound) return;
  window.__exploreBound = true;

  const init = () => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hasObserver = "IntersectionObserver" in window;

    // 创建交叉观察器：只有当卡片进入视口时，才移除 pending 状态触发上滑动画
    const observer = (!reduceMotion && hasObserver) && new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        
        const target = entry.target;
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            target.classList.remove("explore-pending");
            target.classList.add("explore-visible");
          });
        });
        
        obs.unobserve(target);
      });
    }, { 
      threshold: 0.05, 
      rootMargin: "0px 0px 50px 0px" 
    });

    document.querySelectorAll(".explore").forEach(container => {
      container.querySelectorAll("img").forEach(img => {
        if (!img.hasAttribute("loading")) img.loading = "lazy";
        img.decoding = "async";

        // 自动提取 alt 并在图片下方补全标题文字
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

      // 处理每一个卡片的加载与动画入场
      container.querySelectorAll("ul > li").forEach((card) => {
        if (reduceMotion || !hasObserver) {
          card.classList.add("explore-visible");
          return;
        }
        if (card.dataset.exploreRevealReady) return;
        card.dataset.exploreRevealReady = "true";

        // 1. 核心：一开始必须加上 pending 状态（隐藏），彻底杜绝未加载时阴影和文字光秃秃露出的丑陋现象
        card.classList.add("explore-pending");

        const imgs = card.querySelectorAll("img");
        if (imgs.length === 0) {
          observer.observe(card);
          return;
        }

        // 2. 检查图片是否加载完成（兼容缓存和实时加载）
        let loadedCount = 0;
        const checkImagesLoaded = () => {
          loadedCount++;
          if (loadedCount === imgs.length) {
            // 只有当图片（也就是整个卡片的内容）准备就绪后，才交给视口观察器
            // 这样能确保图片、阴影、文字是作为一个整体，在滚动到视口时才一起出现
            observer.observe(card);
          }
        };

        imgs.forEach(img => {
          if (img.complete && img.naturalHeight !== 0) {
            checkImagesLoaded();
          } else {
            img.addEventListener("load", checkImagesLoaded, { once: true });
            img.addEventListener("error", checkImagesLoaded, { once: true });
          }
        });
      });
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