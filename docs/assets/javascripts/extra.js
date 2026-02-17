// 文章中以新标签页打开外部链接
document$.subscribe(function() {
    const content = document.querySelector(".md-typeset");
    if (!content) return;

    content.querySelectorAll('a[href^="http"], a[href^="https"]').forEach(link => {
        if (link.href.startsWith(window.location.origin)) return;

        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
});

// 表格排序
// document$.subscribe(function() {
//   var tables = document.querySelectorAll("article table:not([class])")
//   tables.forEach(function(table) {
//     new Tablesort(table)
//   })
// })

// 数学公式
// window.MathJax = {
//   tex: {
//     inlineMath: [["\\(", "\\)"]],
//     displayMath: [["\\[", "\\]"]],
//     processEscapes: true,
//     processEnvironments: true
//   },
//   options: {
//     ignoreHtmlClass: ".*|",
//     processHtmlClass: "arithmatex"
//   }
// };

// document$.subscribe(() => { 
//   MathJax.startup.output.clearCache()
//   MathJax.typesetClear()
//   MathJax.texReset()
//   MathJax.typesetPromise()
// })