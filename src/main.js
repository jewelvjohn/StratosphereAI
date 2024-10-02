import './main.css'
import './gallery.css'
import "@lottiefiles/lottie-player";
import {create} from '@lottiefiles/lottie-interactivity';
import * as rive from "@rive-app/canvas";

var videoIsPlaying = false;
let buttonPlay, buttonHover;

const instagram = document.getElementById("instagram");
instagram.onload = (e) => {
    create({
        player:'#instagram',
        mode:"cursor",
        actions: [{type: "hold"}]
    });
}

const playPause = new rive.Rive({
    src: './rive/play-pause.riv',
    canvas: document.getElementById('play-pause'),
    autoplay: true,
    stateMachines: 'StateMachine',
    fit: rive.Fit.ScaleDown,
    onLoad: () => {
        playPause.resizeDrawingSurfaceToCanvas(4);
        buttonPlay = playPause.stateMachineInputs('StateMachine').find(i => i.name === 'play');
        buttonHover = playPause.stateMachineInputs('StateMachine').find(i => i.name === 'hover');
    },
});

const videoContainer = document.getElementById("video-container");
const videoPreview = document.getElementById("video-preview");
const videoPlayer = document.getElementById("video-player");
const videoButton = document.getElementById("video-button");

videoButton.addEventListener('mouseenter', () => { if(buttonHover) buttonHover.value = true; });
videoButton.addEventListener('mouseleave', () => { if(buttonHover) buttonHover.value = false; });
videoButton.onclick = toggleVideo;
videoPlayer.volume = 0.5;

function toggleVideo() {
    if(videoIsPlaying) {
        videoPreview.style.display = "flex";
        videoPlayer.style.display = "none";
        videoPlayer.pause();
        previewMode();
        if(buttonPlay) buttonPlay.value = true;
        videoIsPlaying = false;
    } else {
        videoPreview.style.display = "none";
        videoPlayer.style.display = "flex";
        videoPlayer.play();
        videoMode();
        if(buttonPlay) buttonPlay.value = false;
        videoIsPlaying = true;
    }
}

function videoMode() {
    videoContainer.animate([
        {
            border: "2px solid white",
            borderRadius: "32px",
            height: "64px",
            width: "256px",
        },
        {
            border: "1px solid #30475E",
            borderRadius: "16px",
            height: "45vw",
            width: "80vw",
        }
    ], {
        duration: 600,
        fill: "forwards",
        easing: "ease-in-out",
    });
}

function previewMode() {
    videoContainer.animate([
        {
            border: "1px solid #30475E",
            borderRadius: "16px",
            height: "45vw",
            width: "80vw",
        },
        {
            border: "2px solid white",
            borderRadius: "32px",
            height: "64px",
            width: "256px",
        }
    ], {
        duration: 200,
        fill: "forwards",
        easing: "ease-out",
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