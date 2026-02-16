function processLinks() {
    const content = document.querySelector('.md-typeset');
    if (!content) return;

    content.querySelectorAll('a[href^="http"]').forEach(link => {
        if (link.href.startsWith(window.location.origin)) return;

        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
}

function resetLinkState() {
    // 清除焦点
    if (document.activeElement instanceof HTMLElement) {
        document.activeElement.blur();
    }

    // 强制一次 reflow，消掉 active 残留（玄学但有效）
    document.body.offsetHeight;
}

// 初次加载
processLinks();
resetLinkState();

// SPA DOM 监听
const observer = new MutationObserver(() => {
    processLinks();
    resetLinkState();
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
