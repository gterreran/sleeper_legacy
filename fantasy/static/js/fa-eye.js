// fa-eye.js

document.addEventListener('DOMContentLoaded', function() {
  const passwordFields = document.querySelectorAll('[id^="id_password"]');

  passwordFields.forEach(password => {
      const togglePassword = document.querySelector(`#togglePassword${password.id.slice(11) || ''}`);

      if (togglePassword) {
          togglePassword.addEventListener('click', function(e) {
              const type = password.getAttribute('type') === 'text' ? 'password' : 'text';
              password.setAttribute('type', type);
              this.classList.toggle('fa-eye');
              e.preventDefault();
          });
      } else {
          console.error(`Toggle element not found for password field: ${password.id}`);
      }
  });
});