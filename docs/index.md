---
title: liWanr
comments: false
hide: [navigation, toc, path, feedback]
---

<style>
/* ---------- 隐藏不需要的元素 ---------- */
.md-content__button, .headerlink { display: none !important; }
.md-main__inner { margin-top: 0px; }

/* ---------- 基于原生的高度与 containment 控制 ---------- */
body:has(#profile-image) { height: 100vh; overflow: hidden; }
body:has(#profile-image) .md-container,
body:has(#profile-image) .md-main__inner,
body:has(#profile-image) .md-content,
body:has(#profile-image) .md-content__inner { height: 100%; min-height: 0; }

body:has(#profile-image) .md-main { height: calc(100vh - var(--ft-site-header, 95px)); min-height: 0; }

body:has(#profile-image) .md-content__inner { box-sizing: border-box; display: flex; flex-direction: column; }

body:has(#profile-image) .grid.cards { flex: 1; min-height: 0; grid-template-rows: minmax(0, 1fr); align-items: center; }

body:has(#profile-image) #profile-image-container { display: flex; align-items: center; justify-content: center; height: 100%; min-height: 0; }

body:has(#profile-image) #profile-image { display: block; width: auto; height: auto; max-width: 100%; max-height: 100%; object-fit: contain; }

/* ---------- 样式与细节强化 ---------- */

/* 1. 顶部标签（更细的字体） */
.md-typeset .person-tags {
  margin: 0 0 1rem;
  font-size: 0.82rem;
  font-weight: 200;
  letter-spacing: 0.08em;
  color: var(--md-default-fg-color--light);
}
.person-tags span + span::before {
  content: "|";
  margin-inline: 0.85em;
  opacity: 0.45;
}

/* 2. 标题与换行控制 */
.md-typeset .name {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.01em;
  color: var(--md-default-fg-color);
}
.name .hero__br { display: none; }

/* 3. 副标题（颜色与 small 标签一致，恢复斜体） */
.md-typeset .grid.cards em {
  display: block;
  font-size: clamp(1rem, 1.8vw, 1.25rem);
  font-weight: 200;
  line-height: 1.5;
  font-style: italic;
  color: var(--md-default-fg-color--light);
}

/* 4. 社交图标列表（改为清爽的横排平铺，无按钮效果） */
.md-typeset ul.person-links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: .7rem;
  margin: 1rem 0 0 0;
  padding: 0;
  list-style: none;
}
.md-typeset ul.person-links > li { margin: 0; list-style: none; }
.md-typeset .person-links a {
  display: inline-flex;
  align-items: center;
  color: var(--md-default-fg-color--light);
  transition: color 0.2s;
}
.md-typeset .person-links a:hover,
.md-typeset .person-links a:focus-visible {
  color: var(--md-accent-fg-color);
}
.person-links svg { width: 1.35rem; height: 1.35rem; fill: currentColor; }

/* ---------- 移动端布局调整 ---------- */
@media (max-width: 52rem) {
  body:has(#profile-image) { overflow-y: auto; height: auto; }
  body:has(#profile-image) .md-main { height: auto; }
  
  .name .hero__br { display: inline; }
  
  .grid.cards {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 2rem;
    padding: 2rem 0;
  }
  
  .person-tags { margin-inline: auto; }
  ul.person-links { justify-content: center; margin-left: 0; }
}
</style>

<div class="grid cards" markdown>

<div style="margin-bottom: 64px;">
<p class="person-tags"><span>拥有灵魂</span><span>文字</span><span>技术</span><span>记录</span></p>
<h1 class="name">Hello,<span class="hero__br"><br></span> I’m liWanr!</h1>
<em>Every nobody is somebody.</em>

<ul class="person-links">
<li><a href="mailto:itsWanr@iCloud.com" rel="me" title="Email"><span class="twemoji"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M15.61 12c0 1.99-1.62 3.61-3.61 3.61-1.99 0-3.61-1.62-3.61-3.61 0-1.99 1.62-3.61 3.61-3.61 1.99 0 3.61 1.62 3.61 3.61M12 0C5.383 0 0 5.383 0 12s5.383 12 12 12c2.424 0 4.761-.722 6.76-2.087l.034-.024-1.617-1.879-.027.017A9.494 9.494 0 0 1 12 21.54c-5.26 0-9.54-4.28-9.54-9.54 0-5.26 4.28-9.54 9.54-9.54 5.26 0 9.54 4.28 9.54 9.54a9.63 9.63 0 0 1-.225 2.05c-.301 1.239-1.169 1.618-1.82 1.568-.654-.053-1.42-.52-1.426-1.661V12A6.076 6.076 0 0 0 12 5.93 6.076 6.076 0 0 0 5.93 12 6.076 6.076 0 0 0 12 18.07a6.02 6.02 0 0 0 4.3-1.792 3.9 3.9 0 0 0 3.32 1.805c.874 0 1.74-.292 2.437-.821.719-.547 1.256-1.336 1.553-2.285.047-.154.135-.504.135-.507l.002-.013c.175-.76.253-1.52.253-2.457 0-6.617-5.383-12-12-12"/></svg></span></a></li>
<li><a href="https://github.com/liWanr" rel="me" title="GitHub"><span class="twemoji"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.906.614a3.4 3.4 0 0 0-.896.127c-.955.262-1.824.76-2.646 1.302a13.7 13.7 0 0 0-6.807-.002A11 11 0 0 0 6.71 1.016C6.136.78 5.526.585 4.899.622c-.113.01-.263.013-.315.135a5.8 5.8 0 0 0-.422 1.737 4.8 4.8 0 0 0 .223 1.923 5.4 5.4 0 0 0-1.36 3.053c-.05.453-.036.91-.015 1.365-.934-.237-1.93-.278-2.867-.035-.11.025-.174.16-.128.261.036.092.146.14.238.111.912-.232 1.881-.177 2.783.074q.045.412.107.821c-.798-.196-1.635-.093-2.42.11-.14.033-.18.238-.071.328.083.08.205.04.303.015.74-.18 1.536-.258 2.275-.027.072.248.13.5.226.741l.316.715c.321.63.806 1.167 1.365 1.596a6.8 6.8 0 0 0 1.73.942c.727.277 1.49.449 2.258.571a3.3 3.3 0 0 0-.376.498 3.2 3.2 0 0 0-.335.795c-.43.007-.865.05-1.288-.045a1.95 1.95 0 0 1-.864-.452 3.6 3.6 0 0 1-.62-.739 1 1 0 0 0-.618-.43.73.73 0 0 0-.57.11.67.67 0 0 0-.256.406c-.051.221-.011.452.059.665.122.365.351.687.626.954.485.467 1.089.799 1.726 1.006.535.17 1.112.257 1.667.143-.003.99.003 1.979-.003 2.968-.024.232-.134.45-.28.628-.1.128-.23.231-.377.301-.128.056-.268.102-.362.212a.43.43 0 0 0-.097.422.41.41 0 0 0 .265.25c.148.05.306.039.46.036.45-.013.907-.1 1.306-.318.55-.294.95-.897.925-1.532-.002-.679-.022-1.357-.032-2.036-.003-.385-.018-.771.016-1.155.028 1.009.034 2.019.054 3.028.002.324-.001.654-.09.97a1.8 1.8 0 0 1-.365.682c-.098.12-.226.22-.295.362-.06.114-.07.26.001.37.084.143.254.197.409.22.33.041.657-.073.95-.218a2.16 2.16 0 0 0 .86-.783c.209-.338.308-.736.316-1.13.01-.584.008-1.167.017-1.75.035-.297.021-.596.028-.894.005.175.003.35.004.525-.027.534-.003 1.07-.004 1.604.01.31-.013.624.049.93.062.324.195.636.398.897.234.3.551.53.902.678.294.123.63.204.943.105.156-.044.296-.18.3-.35.003-.169-.105-.312-.22-.427a1.87 1.87 0 0 1-.524-1.36V18.47c.004-.27-.012-.54.014-.809.049.405.034.814.033 1.22.004.733-.003 1.466.004 2.2.015.41.18.822.48 1.108.346.337.824.5 1.295.565q.36.05.719.026c.182-.016.37-.137.408-.324.039-.176-.059-.355-.2-.457-.093-.075-.215-.095-.318-.153-.292-.16-.5-.451-.588-.77-.045-.138-.022-.284-.028-.426.001-.89-.007-1.782.008-2.672.483.097.983.043 1.455-.084a4.6 4.6 0 0 0 1.794-.94c.334-.29.618-.651.761-1.073.068-.205.11-.426.068-.641a.7.7 0 0 0-.233-.414.72.72 0 0 0-.583-.137 1 1 0 0 0-.632.431c-.206.314-.445.612-.744.841a1.9 1.9 0 0 1-.718.346c-.43.103-.876.059-1.314.051a3.9 3.9 0 0 0-.72-1.269c-.032-.022.018-.042.036-.041 1.228-.18 2.453-.528 3.514-1.188a5.15 5.15 0 0 0 1.638-1.593 3 3 0 0 0 .21-.383c.096-.214.203-.423.285-.644a8 8 0 0 0 .218-.725c.661-.228 1.38-.193 2.057-.057q.187.037.375.084c.07.017.154.017.21-.036.104-.084.073-.278-.054-.323-.81-.218-1.677-.314-2.5-.104a9 9 0 0 0 .109-.792c0-.031.038-.032.06-.041.903-.252 1.874-.306 2.788-.073.12.038.227-.057.263-.165v-.037c-.031-.073-.074-.156-.16-.173-.956-.246-1.971-.197-2.92.052.038-.68.033-1.37-.125-2.037a5.5 5.5 0 0 0-1.251-2.399c.386-1.133.283-2.39-.134-3.499-.04-.105-.07-.249-.204-.27q-.15-.03-.3-.032"/></svg></span></a></li>
<li><a href="https://t.me/itsWanr" rel="me" title="Telegram"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 8a248 248 0 1 0 0 496 248 248 0 1 0 0-496zM371 176.7c-3.7 39.2-19.9 134.4-28.1 178.3-3.5 18.6-10.3 24.8-16.9 25.4-14.4 1.3-25.3-9.5-39.3-18.7-21.8-14.3-34.2-23.2-55.3-37.2-24.5-16.1-8.6-25 5.3-39.5 3.7-3.8 67.1-61.5 68.3-66.7 .2-.7 .3-3.1-1.2-4.4s-3.6-.8-5.1-.5c-2.2 .5-37.1 23.5-104.6 69.1-9.9 6.8-18.9 10.1-26.9 9.9-8.9-.2-25.9-5-38.6-9.1-15.5-5-27.9-7.7-26.8-16.3 .6-4.5 6.7-9 18.4-13.7 72.3-31.5 120.5-52.3 144.6-62.3 68.9-28.6 83.2-33.6 92.5-33.8 2.1 0 6.6 .5 9.6 2.9 2 1.7 3.2 4.1 3.5 6.7 .5 3.2 .6 6.5 .4 9.8z"/></svg></span></a></li>
<li><a href="https://youtube.com/channel/UCxWDG44qmWb0waYIu0XY8VQ" rel="me" title="YouTube"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M549.7 124.1C543.5 100.4 524.9 81.8 501.4 75.5 458.9 64 288.1 64 288.1 64S117.3 64 74.7 75.5C51.2 81.8 32.7 100.4 26.4 124.1 15 167 15 256.4 15 256.4s0 89.4 11.4 132.3c6.3 23.6 24.8 41.5 48.3 47.8 42.6 11.5 213.4 11.5 213.4 11.5s170.8 0 213.4-11.5c23.5-6.3 42-24.2 48.3-47.8 11.4-42.9 11.4-132.3 11.4-132.3s0-89.4-11.4-132.3zM232.2 337.6l0-162.4 142.7 81.2-142.7 81.2z"/></svg></span></a></li>
<li><a href="https://gravatar.com/liwanr" rel="me" title="Steam"><span class="twemoji"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M11.979 0C5.678 0 .511 4.86.022 11.037l6.432 2.658c.545-.371 1.203-.59 1.912-.59.063 0 .125.004.188.006l2.861-4.142V8.91c0-2.495 2.028-4.524 4.524-4.524 2.494 0 4.524 2.031 4.524 4.527s-2.03 4.525-4.524 4.525h-.105l-4.076 2.911c0 .052.004.105.004.159 0 1.875-1.515 3.396-3.39 3.396-1.635 0-3.016-1.173-3.331-2.727L.436 15.27C1.862 20.307 6.486 24 11.979 24c6.627 0 11.999-5.373 11.999-12S18.605 0 11.979 0zM7.54 18.21l-1.473-.61c.262.543.714.999 1.314 1.25 1.297.539 2.793-.076 3.332-1.375.263-.63.264-1.319.005-1.949s-.75-1.121-1.377-1.383c-.624-.26-1.29-.249-1.878-.03l1.523.63c.956.4 1.409 1.5 1.009 2.455-.397.957-1.497 1.41-2.454 1.012H7.54zm11.415-9.303c0-1.662-1.353-3.015-3.015-3.015-1.665 0-3.015 1.353-3.015 3.015 0 1.665 1.35 3.015 3.015 3.015 1.663 0 3.015-1.35 3.015-3.015zm-5.273-.005c0-1.252 1.013-2.266 2.265-2.266 1.249 0 2.266 1.014 2.266 2.266 0 1.251-1.017 2.265-2.266 2.265-1.253 0-2.265-1.014-2.265-2.265z"/></svg></span></a></li>
<li><a href="https://gravatar.com/liwanr" rel="me" title="Gravatar"><span class="twemoji"><svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0c-1.326 0-2.4 1.074-2.4 2.4v8.4c0 1.324 1.074 2.398 2.4 2.398s2.4-1.074 2.4-2.398V5.21c2.795.99 4.799 3.654 4.799 6.789 0 3.975-3.225 7.199-7.199 7.199S4.801 15.975 4.801 12c0-1.989.805-3.789 2.108-5.091.938-.938.938-2.458 0-3.396s-2.458-.938-3.396 0C1.344 5.686 0 8.686 0 12c0 6.627 5.373 12 12 12s12-5.373 12-12S18.627 0 12 0"/></svg></span></a></li>
<li><a href="/recom/links/" title="Links"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M64 128a112 112 0 1 1 224 0 112 112 0 1 1 -224 0zM0 464c0-97.2 78.8-176 176-176s176 78.8 176 176l0 6c0 23.2-18.8 42-42 42L42 512c-23.2 0-42-18.8-42-42l0-6zM432 64a96 96 0 1 1 0 192 96 96 0 1 1 0-192zm0 240c79.5 0 144 64.5 144 144l0 22.4c0 23-18.6 41.6-41.6 41.6l-144.8 0c6.6-12.5 10.4-26.8 10.4-42l0-6c0-51.5-17.4-98.9-46.5-136.7 22.6-14.7 49.6-23.3 78.5-23.3z"/></svg></span></a></li>
</ul>
</div>

<div id="profile-image-container">
  <img class="movie-links" 
    src="/assets/images/index/me.png" 
    alt="liWanr 的肖像" id="profile-image">
</div>

</div>