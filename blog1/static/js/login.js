// Flash messages animation
const flashMessages = document.querySelectorAll('.flash');
flashMessages.forEach((message) => {
    message.style.display = 'block';
    setTimeout(() => {
        message.style.display = 'none';
    }, 5000);
});

// Password strength indicator
const passwordInput = document.getElementById('password');
const strengthMeter = document.querySelector('.strength-meter');

passwordInput.addEventListener('input', function() {
    const password = this.value;
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    
    strengthMeter.className = 'strength-meter';
    if (strength === 1) strengthMeter.classList.add('weak');
    else if (strength === 2) strengthMeter.classList.add('medium');
    else if (strength === 3) strengthMeter.classList.add('strong');
});