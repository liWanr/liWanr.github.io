let rssRingTurnstileToken = '';

function rssRingOnVerified(token) {
  rssRingTurnstileToken = token;
  document.getElementById('rss-ring-submit').disabled = false;
}

function rssRingOnExpired() {
  rssRingTurnstileToken = '';
  document.getElementById('rss-ring-submit').disabled = true;
}

document.getElementById('rss-ring-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const email = document.getElementById('bd-email').value;
  const messageEl = document.getElementById('rss-ring-message');

  if (!rssRingTurnstileToken) {
    messageEl.textContent = '请先完成人机验证';
    return;
  }

  messageEl.textContent = '提交中...';

  try {
    const resp = await fetch('https://rss-ring.itswanr.workers.dev/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, turnstileToken: rssRingTurnstileToken }),
    });
    const data = await resp.json();
    messageEl.textContent = data.message;
  } catch (err) {
    messageEl.textContent = '提交失败，请稍后重试';
  } finally {
    turnstile.reset();
    rssRingOnExpired();
  }
});