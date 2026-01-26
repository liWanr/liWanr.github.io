// 文章中以新标签页打开外部链接
document.addEventListener('DOMContentLoaded', function() {
    const content = document.querySelector('.md-typeset');
    if (!content) return;

    content.querySelectorAll('a[href^="http"], a[href^="https"]').forEach(link => {
        if (link.href.startsWith(window.location.origin)) return;

        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
});