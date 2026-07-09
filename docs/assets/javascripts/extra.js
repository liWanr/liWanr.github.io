document.addEventListener('click', function(e) {
    const link = e.target.closest('a[href^="http"], a[href^="https"]');
    if (!link) return;
    else if (link.href.startsWith(window.location.origin)) return;
    else if (link.classList.contains('glightbox')) return;

    e.preventDefault();
    window.open(link.href, '_blank', 'noopener,noreferrer');
});