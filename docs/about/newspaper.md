---
title: 新闻简报
hide:
    - path
---

<style>
.mdx-form__input--stretch {
    width: 50%;
}

.mdx-form__input {
    background-color: var(--md-default-fg-color--lightest);
    border-radius: .5rem;
    flex: 1 1 50%;
    font-size: 14px;
    line-height: 1.4;
    min-width: 0;
    padding: .5rem 1rem;
}

#rss-ring-submit:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<p id="rss-ring-message">内容更新不会等你，但订阅可以。</p>

<form id="rss-ring-form">
  <div style="display: flex; gap: 8px; align-items: center;">
    <input class="mdx-form__input mdx-form__input--stretch" type="email" name="email" id="bd-email" style="flex: 1;"  placeholder="your-email@example.com" autocomplete="email" required/>
    <button class="md-button md-button--primary" type="submit" id="rss-ring-submit" disabled>订阅</button>
  </div>
  <div class="cf-turnstile"
       data-sitekey="0x4AAAAAADwZnEQiPgcV_V17"
       data-callback="rssRingOnVerified"
       data-expired-callback="rssRingOnExpired"
       data-error-callback="rssRingOnExpired"></div>
</form>

<script src="/assets/javascripts/about.js"></script>
