document.addEventListener('DOMContentLoaded', function() {
    const bubbleContainers = document.querySelectorAll('.navbar');
    
    const bubble_images = [
        '/static/img/header/bubbles/bubble1.png',
        '/static/img/header/bubbles/bubble2.png',
        '/static/img/header/bubbles/bubble3.png',
    ];

    bubbleContainers.forEach(function(container) {

        const bubble_count = 16;
    
        for(let i = 0; i < bubble_count; i++) {
        const bubble = document.createElement("img");

        bubble.src = bubble_images[Math.floor(Math.random() * bubble_images.length)];
        bubble.className = "bubble";

        bubble.style.left = Math.random() * 100 + "%";
        bubble.style.top = (Math.random() + 2 )* 50 + "%";
        bubble.style.scale = Math.random() * 0.5 + 0.2;
        
        // Randomize animation delay and duration
        bubble.style.animationDelay = Math.random() * 2 + "s";
        bubble.style.animationDuration = (Math.random() * 2 + 3) + "s";
        
        container.appendChild(bubble);
        }
    });
});