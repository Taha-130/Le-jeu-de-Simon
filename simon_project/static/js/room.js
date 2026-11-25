const slots = document.querySelectorAll(".slot");
const info = document.getElementById("info");
const startButton = document.getElementById("start");

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

if (startButton) {
    startButton.addEventListener("click", function () {
        socket.send(JSON.stringify({ type: "start" }));
    });
}

function displayPlayers(players) {
    for (let i = 0; i < slots.length; i++) {
        if (players[i]) {
            slots[i].classList.remove("empty");
            slots[i].classList.add("full");
            slots[i].textContent = players[i];
        } else {
            slots[i].classList.remove("full");
            slots[i].classList.add("empty");
            slots[i].textContent = "Waiting...";
        }
    }
}