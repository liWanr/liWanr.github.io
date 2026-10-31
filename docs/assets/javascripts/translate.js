document.addEventListener("DOMContentLoaded", function() {
  if (typeof OpenCC === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/opencc-js@1.0.5/dist/umd/full.js';
    script.async = true;
    script.onload = initTranslator;
    document.head.appendChild(script);
  } else {
    initTranslator();
  }

  function initTranslator() {
    const toTraditional = OpenCC.Converter({ from: 'cn', to: 't' });
    let isTraditional = false;
    const btn = document.getElementById('zh-convert-btn');

    // 获取目标容器
    const getContainers = () => document.querySelectorAll(
      '.md-content__inner.md-typeset, .md-nav.md-nav--secondary .md-nav__title ~ .md-nav__list'
    );

    // 1. 在页面加载时，把指定区域内所有文本节点的“原始简体”备份下来
    const textNodeCache = new Map();
    getContainers().forEach(container => {
      const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
        acceptNode: function(node) {
          if (['SCRIPT', 'STYLE', 'CODE', 'PRE'].includes(node.parentNode.tagName) || node.parentNode.id === 'zh-convert-btn') {
            return NodeFilter.FILTER_REJECT;
          }
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      while (walker.nextNode()) {
        textNodeCache.set(walker.currentNode, walker.currentNode.nodeValue);
      }
    });

    // 2. 点击按钮时切换
    window.toggleLanguage = function() {
      isTraditional = !isTraditional;
      
      textNodeCache.forEach((originalText, node) => {
        if (isTraditional) {
          // 转为繁体：基于最原始的简体进行转换
          node.nodeValue = toTraditional(originalText);
        } else {
          // 切回简体：直接还原最开始缓存的原文，绝不二次翻译！
          node.nodeValue = originalText;
        }
      });

      if (btn) {
        btn.innerText = isTraditional ? '简体中文' : '繁體中文';
      }
    };
  }
});