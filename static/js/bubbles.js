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
        bubble.setAttribute("id",  "bubble_" + i);

        bubble.onclick = bubble_pop(bubble.id);

        bubble.style.position = "absolute";
        bubble.style.width = "50px";
        bubble.style.height = "auto";
        bubble.style.zIndex = -10;
        bubble.filter.brightness = "var(--bubble-brightness)";

        bubble.style.left = Math.random() * 100 + "%";
        bubble.style.top = (Math.random() + 2 )* 50 + "%";
        bubble.style.scale = Math.random() * 1.5 + 0.2;
        
        // Randomize animation delay and duration
        bubble.style.animationDelay = Math.random() * 2 + "s";
        bubble.style.animationDuration = (Math.random() * 2 + 3) + "s";
        
        container.appendChild(bubble);
        }

    });
    
    function bubble_pop(bubble_id){
        const popped_bubble = document.getElementById(bubble_id);
        alert("test")
    }

});