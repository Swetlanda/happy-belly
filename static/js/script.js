// Log a message to ensure the script is loaded
console.log("script.js loaded successfully.");

// JavaScript functionality: Change the background color of the body on load
document.addEventListener('DOMContentLoaded', function() {
    document.body.style.backgroundColor = '#f0f0f0'; 
});

document.querySelectorAll('.card').forEach(card => {
    card.style.display = 'block'; // Force display for debugging
});