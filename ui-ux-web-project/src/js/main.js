// This file contains the main JavaScript logic for the web application, handling interactions and dynamic content.

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document is ready!');

    // Example: Add event listeners for buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            alert(`Button ${button.textContent} clicked!`);
        });
    });

    // Example: Dynamic content loading
    const loadContent = (page) => {
        fetch(`./pages/${page}.html`)
            .then(response => response.text())
            .then(data => {
                document.getElementById('content').innerHTML = data;
            })
            .catch(error => console.error('Error loading content:', error));
    };

    // Load default content
    loadContent('about'); // Change to 'contact' or other pages as needed
});