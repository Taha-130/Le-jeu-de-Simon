const slots = document.querySelectorAll(".slot");
const info = document.getElementById("info");
const boutonStart = document.getElementById("start");

const socket = new WebSocket("ws://" + location.host + "/ws/simon/" + code + "/");

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "players_update") {
        displayPlayers(data.players);
    }
    if (data.type === "game_started") {
        window.location.href = "/lobby/" + code + "/play/";
    }
    if (data.type === "error") {
        info.textContent = data.message;
    }
};

if (boutonStart) {
    boutonStart.addEventListener("click", function () {
        socket.send(JSON.stringify({ type: "start" }));
    });
}

function displayPlayers(players) {
    for (let i = 0; i < slots.length; i++) {
        if (players[i]) {
            slots[i].classList.remove("vide");
            slots[i].classList.add("plein");
            slots[i].textContent = players[i];
        } else {
            slots[i].classList.remove("plein");
            slots[i].classList.add("vide");
            slots[i].textContent = "Waiting...";
        }
    }
}