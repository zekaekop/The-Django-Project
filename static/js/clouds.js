document.addEventListener('DOMContentLoaded', function() {
    const cloudContainers = document.querySelectorAll('.container');
    
    const cloud_images = [
        '/static/img/clouds/cloud1.png',
        '/static/img/clouds/cloud2.png',
        '/static/img/clouds/cloud3.png',
        '/static/img/clouds/cloud4.png',
    ];

    cloudContainers.forEach(function(container) {

        const cloud_count = 16;
    
        for(let i = 0; i < cloud_count; i++) {
        const cloud = document.createElement("img");

        cloud.src = cloud_images[Math.floor(Math.random() * cloud_images.length)];
        cloud.className = "cloud";

        cloud.style.left = Math.random() * 80 + "%";
        cloud.style.top = Math.random() * 30 + "%";
        cloud.style.scale = Math.random() * 0.5 + 0.2;
        
        // Randomize animation delay and duration
        cloud.style.animationDelay = Math.random() * 2 + "s";
        cloud.style.animationDuration = (Math.random() * 2 + 3) + "s";
        
        container.appendChild(cloud);
        }
    });
});