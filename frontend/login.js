const SESSION_KEY = 'skillmatch-demo-email';

if (sessionStorage.getItem(SESSION_KEY)) {
  window.location.replace('index.html');
}

document.getElementById('login-form').addEventListener('submit', (event) => {
  event.preventDefault();

  const emailInput = document.getElementById('login-email');
  const email = emailInput.value.trim();
  const errorMessage = document.getElementById('login-error');

  if (!emailInput.validity.valid || !email) {
    errorMessage.textContent = 'Enter a valid email address to continue.';
    emailInput.focus();
    return;
  }

  sessionStorage.setItem(SESSION_KEY, email);
  window.location.assign('index.html');
});
