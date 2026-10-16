const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
let turnstileToken = '';

const emailEl = document.getElementById('bd-email');
const privacyEl = document.getElementById('rss-ring-privacy-checkbox');
const submitBtn = document.getElementById('rss-ring-submit');
const messageEl = document.getElementById('rss-ring-message');

function updateState() {
  submitBtn.disabled = !(EMAIL_REGEX.test(emailEl.value.trim()) && turnstileToken && privacyEl.checked);
}

emailEl.addEventListener('input', updateState);
privacyEl.addEventListener('change', updateState);

window.rssRingOnVerified = (token) => { turnstileToken = token; updateState(); };
window.rssRingOnExpired = () => { turnstileToken = ''; updateState(); };

document.getElementById('rss-ring-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = emailEl.value.trim();

  if (!EMAIL_REGEX.test(email)) return messageEl.textContent = '邮箱格式不正确，请检查后重试';
  if (!privacyEl.checked) return messageEl.textContent = '请先阅读并勾选同意隐私政策';
  if (!turnstileToken) return messageEl.textContent = '请等待人机验证...如果长时间未响应，请刷新页面重试';

  messageEl.textContent = '提交中，请稍后...如果长时间未响应，请刷新页面重试';

  try {
    const resp = await fetch('https://rss-ring.itswanr.workers.dev/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, turnstileToken }),
    });
    const data = await resp.json();
    messageEl.textContent = data.message;
  } catch {
    messageEl.textContent = '提交失败，请稍后重试';
  } finally {
    turnstile.reset();
    rssRingOnExpired();
  }
});