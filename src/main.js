import './main.css'
import './gallery.css'
import "@lottiefiles/lottie-player";
import {create} from '@lottiefiles/lottie-interactivity';

const instagram = document.getElementById("instagram");
instagram.onload = (e) => {
    create({
        player:'#instagram',
        mode:"cursor",
        actions: [{type: "hold"}]
    });
}

const panels = document.querySelectorAll(".panel");

panels.forEach((panel) => {
    panel.addEventListener("click", () => {
        removeActiveClasses();
        panel.classList.add("active");
    });
});

function removeActiveClasses() {
    panels.forEach((panel) => {
        panel.classList.remove("active");
    });
}