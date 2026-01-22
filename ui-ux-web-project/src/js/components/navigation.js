const navigationMenu = document.querySelector('.navigation-menu');
const navToggle = document.querySelector('.nav-toggle');

navToggle.addEventListener('click', () => {
    navigationMenu.classList.toggle('active');
});

document.querySelectorAll('.navigation-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navigationMenu.classList.remove('active');
    });
});