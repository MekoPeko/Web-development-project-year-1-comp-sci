// Student ID - 2400965 , Student name - Harry Masters 
// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            const navbarLinks = document.getElementById('navbar-links');
            if (navbarLinks) {
                navbarLinks.classList.toggle('active');
            }
        });
    }
});
