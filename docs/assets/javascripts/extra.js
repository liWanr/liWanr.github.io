document.addEventListener('click', function(e) {
    const link = e.target.closest('a[href^="http"], a[href^="https"]');
    if (!link) return;
    if (link.href.startsWith(window.location.origin)) return;

    e.preventDefault();
    window.open(link.href, '_blank', 'noopener,noreferrer');
});