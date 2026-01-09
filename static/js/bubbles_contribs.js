document.addEventListener('DOMContentLoaded', function() {
    const bubbleContainers = document.querySelectorAll('.container');
    
    const bubble_images = [
        '/static/img/header/bubbles/bubble1.png',
        '/static/img/header/bubbles/bubble2.png',
        '/static/img/header/bubbles/bubble3.png',
    ];

    const bubble_half_broken_images = [
        '/static/img/header/bubbles/bubble1_half_broken.png',
        '/static/img/header/bubbles/bubble2_half_broken.png',
        '/static/img/header/bubbles/bubble3_half_broken.png',
    ];

    const bubble_broken_images = [
        '/static/img/header/bubbles/bubble1_broken.png',
        '/static/img/header/bubbles/bubble2_broken.png',
        '/static/img/header/bubbles/bubble3_broken.png',
    ];

    bubbleContainers.forEach(function(container) {

        const bubble_count = 16;
    
        for(let i = 0; i < bubble_count; i++) {
        const bubble = document.createElement("img");

        bubble.src = bubble_images[Math.floor(Math.random() * bubble_images.length)];
        bubble.setAttribute("id",  "bubble_" + i);
        bubble.setAttribute("class", "bubble_contrib");

        bubble.onclick = function() { 
            bubble_pop(this.id);
         }

        bubble.style.left = Math.random() * 100 + "%";
        bubble.style.top = (Math.random() ) * 100 + "%";
        bubble.style.scale = Math.random() * 2.5 + 1.5;
        
        // Randomize animation delay and duration
        bubble.style.animationDelay = Math.random() * 2 + "s";
        bubble.style.animationDuration = (Math.random() * 12 + 5) + "s";
        
        container.appendChild(bubble);
        }
    });

    const bubble_pop = async (bubble_id) => {
        const popped_bubble = document.getElementById(bubble_id);
        var path = popped_bubble.src.split("/");
        var last_path = path[path.length-1];

        if (last_path == "bubble1.png") {
            popped_bubble.src = bubble_half_broken_images[0];
            await delay(50);
            popped_bubble.src = bubble_broken_images[0];
            await delay(50);
            popped_bubble.remove();
        }
        else if (last_path == "bubble2.png"){
            popped_bubble.src = bubble_half_broken_images[1];
            await delay(50);
            popped_bubble.src = bubble_broken_images[1];
            await delay(50);
            popped_bubble.remove();
        }
        else if (last_path == "bubble3.png"){
            popped_bubble.src = bubble_half_broken_images[2];
            await delay(50);
            popped_bubble.src = bubble_broken_images[2];
            await delay(50);
            popped_bubble.remove();
        }
    }

    function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
    }

});