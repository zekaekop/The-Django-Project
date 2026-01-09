var clicks = 0;

const fake_boat = document.getElementById("home_boat");
const real_boat = document.getElementById("credit_boat");

function damage_boat(){
    if (window.location.pathname != "/credits/thank-you"){
        fake_boat.style.transform = "rotate(" + (Math.random() * 50 + -30) + "deg)";

        clicks += 1;
        breaking_sprties = "/static/img/header/boat_sail_dmg"

        switch (clicks){
            case 1:
                change_boat_sprite(clicks);
                break;
            case 2:
                change_boat_sprite(clicks);
                break;
            case 3:
                change_boat_sprite(clicks);
                break;
            case 4:
                change_boat_sprite(clicks);
                break;
            default:
                change_boat_sprite(0);
        }
        if (clicks >= 4){
            credit_boat();
        }
    }
}

function change_boat_sprite(i){
    fake_boat.src = breaking_sprties + i + ".png";
}

function credit_boat(){
        const fake_boat = document.getElementById("home_boat"); 
        real_boat.style.display = "block";
        fake_boat.style.display = "none";
}