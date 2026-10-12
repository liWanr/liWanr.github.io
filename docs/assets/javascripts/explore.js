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

      container.querySelectorAll("ul > li").forEach((card, index) => {
        if (reduceMotion || !hasObserver) {
          card.classList.add("explore-visible");
          return;
        }
        if (card.dataset.exploreRevealReady) return;
        card.dataset.exploreRevealReady = "true";

        card.classList.add("explore-pending");
        card.style.transitionDelay = `${(index % 6) * 45}ms`;

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