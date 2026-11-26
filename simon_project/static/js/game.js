const playersDiv = document.getElementById("players");
const info = document.getElementById("info");
const alert = document.getElementById("alert");
const board = document.getElementById("board");
const homeLink = document.getElementById("home-link");
const loading = document.getElementById("loading");
const colorButtons = document.querySelectorAll(".simon");

const audioContext = new AudioContext();
const notes = {
    red: 524,
    blue: 660,
    yellow: 784,
    green: 1046,
};

setTimeout(function () {
    loading.classList.add("d-none");
}, 3000);

const socket = new WebSocket("ws://" + location.host + "/ws/simon/" + code + "/");

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "state") {
        displayState(data);
    }
    if (data.type === "color_played") {
        lightsOn(data.color);
        if (data.wrong) {
            alert.textContent = data.player + " made a mistake (" + data.color + ") and is eliminated !";
        } else {
            alert.textContent = data.player + " played " + data.color;
        }
    }
    if (data.type === "error") {
        alert.textContent = data.message;
    }
};

colorButtons.forEach(function (bouton) {
    bouton.addEventListener("click", function () {
        socket.send(JSON.stringify({ type: "color", color: bouton.dataset.color }));
    });
});

function displayState(data) {
    playersDiv.innerHTML = "";
    data.players.forEach(function (p) {
        const card = document.createElement("div");
        card.className = "full slot";
        if (p.eliminated) card.classList.add("eliminated");
        if (p.name === data.current && !data.winner) card.classList.add("active");
        card.textContent = p.name;
        playersDiv.appendChild(card);
    });

    const myPlayer = data.players.find(function (p) { return p.name === me; });

    board.classList.add("inactive");

    if (data.winner) {
        info.textContent = data.winner === me ? "You won!" : data.winner + " has won the game!";
        homeLink.classList.remove("d-none");
    } else if (myPlayer && myPlayer.eliminated) {
        info.textContent = "You are eliminated, you are watching the rest of the game.";
    } else if (data.current === me) {
        board.classList.remove("inactive");
        info.textContent = "It's your turn to play! (" + data.length + " color(s) to reproduce)";
    } else {
        info.textContent = "It's " + data.current + "'s turn to play.";
    }
}

window.addEventListener("pointerdown", function unlockAudio() {
    if (audioContext.state === "suspended") {
        audioContext.resume();
    }
}, { once: true });

function playTone(color) {
    const frequency = notes[color];
    if (!frequency || audioContext.state !== "running") return;

    const oscillator = audioContext.createOscillator();
    const volume = audioContext.createGain();

    oscillator.frequency.value = frequency;
    volume.gain.setValueAtTime(0.15, audioContext.currentTime);
    volume.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.18);

    oscillator.connect(volume);
    volume.connect(audioContext.destination);
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.18);
}

function lightsOn(color) {
    const bouton = document.querySelector(".simon." + color);
    playTone(color);
    bouton.classList.add("lights_on");
    setTimeout(function () {
        bouton.classList.remove("lights_on");
    }, 300);
}
