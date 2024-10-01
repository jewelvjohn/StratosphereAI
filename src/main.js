import './style.css'
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