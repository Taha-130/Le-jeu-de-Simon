const slots = document.querySelectorAll(".slot");
const socket = new WebSocket("ws://" + location.host + "/ws/simon/" + code + "/");
const info = document.getElementById("info");
const boutonStart = document.getElementById("start");

if (boutonStart) {
    boutonStart.addEventListener("click", function () {
        socket.send(JSON.stringify({ type: "start" }));
    });
}

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "players_update") {
        afficherJoueurs(data.players);
    }
    if (data.type === "game_started") {
        info.textContent = "La partie commence ! C'est à " + data.player + " de jouer.";
        if (boutonStart) boutonStart.remove();
    }
    if (data.type === "error") {
        info.textContent = data.message;
    }
};

function afficherJoueurs(joueurs) {
    for (let i = 0; i < slots.length; i++) {
        if (joueurs[i]) {
            slots[i].className = "slot border rounded p-5 bg-success text-white";
            slots[i].textContent = joueurs[i];
        } else {
            slots[i].className = "slot border rounded p-5 text-muted";
            slots[i].textContent = "Waiting…";
        }
    }
}