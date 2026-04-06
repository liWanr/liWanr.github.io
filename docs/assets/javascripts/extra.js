document$.subscribe(function() {
    const content = document.querySelector(".md-typeset");
    if (!content) return;
    content.querySelectorAll('a[href^="http"], a[href^="https"]').forEach(link => {
        if (link.href.startsWith(window.location.origin)) return;

        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });

    const travellingUrl = "https://www.travellings.cn/go.html";
    document.querySelectorAll(`a[href="${travellingUrl}"]`).forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
});