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
        card.classList.add("explore-pending");
        card.style.transitionDelay = `${(index % 6) * 45}ms`;
        observer.observe(card);
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