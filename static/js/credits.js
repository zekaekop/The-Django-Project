var clicks = 0

const fake_boat = document.getElementById("home_boat");
const real_boat = document.getElementById("credit_boat");

function damage_boat(){
    if (window.location.pathname != "/credits/thank-you"){
        fake_boat.style.transform = "rotate(" + (Math.random() * 50 + -30) + "deg)";

        clicks += 1;

        if (clicks >= 2){
            credit_boat();
        }
    }
}

function credit_boat(){
        const fake_boat = document.getElementById("home_boat"); 
        real_boat.style.display = "block";
        fake_boat.style.display = "none";
}