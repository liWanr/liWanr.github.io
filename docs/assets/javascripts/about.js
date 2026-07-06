const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

let rssRingTurnstileToken = '';
let rssRingEmailValid = false;

function rssRingUpdateSubmitState() {
  document.getElementById('rss-ring-submit').disabled = !(rssRingEmailValid && rssRingTurnstileToken);
}

document.getElementById('bd-email').addEventListener('input', function (e) {
  rssRingEmailValid = EMAIL_REGEX.test(e.target.value.trim());
  rssRingUpdateSubmitState();
});

function rssRingOnVerified(token) {
  rssRingTurnstileToken = token;
  rssRingUpdateSubmitState();
}

function rssRingOnExpired() {
  rssRingTurnstileToken = '';
  rssRingUpdateSubmitState();
}

document.getElementById('rss-ring-form').addEventListener('submit', async function (e) {
  e.preventDefault();
  const email = document.getElementById('bd-email').value;
  const messageEl = document.getElementById('rss-ring-message');

  if (!rssRingEmailValid) {
    messageEl.textContent = '邮箱格式不正确，请检查后重试';
    return;
  }

  if (!rssRingTurnstileToken) {
    messageEl.textContent = '请等待人机验证...';
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