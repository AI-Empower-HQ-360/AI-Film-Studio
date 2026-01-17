/**
 * AI Film Studio - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Update aria-expanded attribute for accessibility
            const isExpanded = navLinks.classList.contains('active');
            navToggle.setAttribute('aria-expanded', isExpanded);
        });

        // Close mobile menu when clicking on a link
        const links = navLinks.querySelectorAll('a');
        links.forEach(function(link) {
            link.addEventListener('click', function() {
                navLinks.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navToggle.contains(event.target) && !navLinks.contains(event.target)) {
                navLinks.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Smooth scroll for documentation sidebar links
    const docsSidebarLinks = document.querySelectorAll('.docs-nav a[href^="#"]');
    docsSidebarLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Highlight current section in docs sidebar
    function highlightCurrentSection() {
        const sections = document.querySelectorAll('.docs-section[id]');
        const sidebarLinks = document.querySelectorAll('.docs-nav a');
        
        if (sections.length === 0 || sidebarLinks.length === 0) return;

        const headerHeight = document.querySelector('.header').offsetHeight;
        const scrollPosition = window.scrollY + headerHeight + 50;

        sections.forEach(function(section) {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                sidebarLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + sectionId) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    // Add scroll listener for docs page
    if (document.querySelector('.docs-layout')) {
        window.addEventListener('scroll', highlightCurrentSection);
        highlightCurrentSection();
    }
});
