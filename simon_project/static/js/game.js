const playersDiv = document.getElementById("players");
const info = document.getElementById("info");
const alert = document.getElementById("alert");
const board = document.getElementById("board");
const homeLink = document.getElementById("home-link");
const loading = document.getElementById("loading");
const colorButtons = document.querySelectorAll(".simon");

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

    const moiJoueur = data.players.find(function (p) { return p.name === moi; });

    board.classList.add("inactive");

    if (data.winner) {
        info.textContent = data.winner === moi ? "You won!" : data.winner + " has won the game!";
        homeLink.classList.remove("d-none");
    } else if (moiJoueur && moiJoueur.eliminated) {
        info.textContent = "You are eliminated, you are watching the rest of the game.";
    } else if (data.current === moi) {
        board.classList.remove("inactive");
        info.textContent = "It's your turn to play! (" + data.length + " color(s) to reproduce)";
    } else {
        info.textContent = "It's " + data.current + "'s turn to play.";
    }
}

function lightsOn(color) {
    const bouton = document.querySelector(".simon." + color);
    bouton.classList.add("lights_on");
    setTimeout(function () {
        bouton.classList.remove("lights_on");
    }, 800);
}