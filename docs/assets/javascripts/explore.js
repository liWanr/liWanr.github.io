(() => {
  if (window.__exploreBound) return;
  window.__exploreBound = true;

  const init = () => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const hasObserver = "IntersectionObserver" in window;

    const observer = (!reduceMotion && hasObserver) && new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            entry.target.classList.remove("explore-pending");
            entry.target.classList.add("explore-visible");
            entry.target.style.transitionDelay = "";
          });
        });
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: "0px 0px 40px 0px" });

    document.querySelectorAll(".explore").forEach(container => {
      container.querySelectorAll("img").forEach(img => {
        if (!img.hasAttribute("loading")) img.loading = "lazy";
        img.decoding = "async";
      });

      container.querySelectorAll("ul > li").forEach((card, index) => {
        if (reduceMotion || !hasObserver) {
          card.classList.add("explore-visible");
          return;
        }
        if (card.dataset.exploreRevealReady) return;
        card.dataset.exploreRevealReady = "true";

        // 先设为 pending 状态（透明、下沉），等待图片加载
        card.classList.add("explore-pending");
        card.style.transitionDelay = `${(index % 6) * 45}ms`;

        // 检查卡片内的所有图片是否加载完成
        const imgs = card.querySelectorAll("img");
        if (imgs.length === 0) {
          observer.observe(card);
          return;
        }

        let loadedCount = 0;
        const checkImagesLoaded = () => {
          loadedCount++;
          if (loadedCount === imgs.length) {
            observer.observe(card);
          }
        };

        imgs.forEach(img => {
          // 如果图片已经缓存并加载完成，或者通过其他方式直接 complete
          if (img.complete && img.naturalHeight !== 0) {
            checkImagesLoaded();
          } else {
            // 绑定一次性 load 事件，同时加上 error 兜底，防止图片加载失败时卡片永远出不来
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