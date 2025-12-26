document.addEventListener('DOMContentLoaded', function() {
    const cloudContainers = document.querySelectorAll('body');
    
    const cloud_images = [
        '/static/img/clouds/cloud1_trans.png',
        // '/static/img/clouds/cloud2.png',
        // '/static/img/clouds/cloud3.png',
        // '/static/img/clouds/cloud4.png',
    ];

    cloudContainers.forEach(function(container) {

        const cloud_count = 8;
    
        for(let i = 0; i < cloud_count; i++) {
        const cloud = document.createElement("img");

        cloud.src = cloud_images[Math.floor(Math.random() * cloud_images.length)];
        cloud.className = "cloud";

        cloud.style.left = Math.random() * -10 + - 10 +  "%";
        cloud.style.top = Math.random() * 70 + 10 + "%";
        cloud.style.scale = Math.random() * 0.5 + 0.2;
        
        // Randomize animation delay and duration
        cloud.style.animationDelay = (Math.random() * 10)+ "s";
        cloud.style.animationDuration = (Math.random() * 20 + 30) + "s";
        
        container.appendChild(cloud);
        }
    });
});