function validateLogin() {
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const errorMsg = document.getElementById('error-msg');

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  // Basic email regex for validation
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailPattern.test(email)) {
    errorMsg.textContent = 'Please enter a valid email address.';
    emailInput.focus();
    return false;
  }

  if (password.length < 6) {
    errorMsg.textContent = 'Password must be at least 6 characters.';
    passwordInput.focus();
    return false;
  }

  // Clear error message
  errorMsg.textContent = '';

  // Here you would normally send data to backend and check login
  alert('Login successful! (Simulation)');

  // Return true to submit form or false if you want to block
  // For now, prevent actual submission for demo:
  return false;
}
