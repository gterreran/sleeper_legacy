document.addEventListener('DOMContentLoaded', function() {
    const triggers = document.querySelectorAll('.sleeper-user-trigger');

    triggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const dropdown = this.parentElement;
            dropdown.classList.toggle('show');
        });
    });
});