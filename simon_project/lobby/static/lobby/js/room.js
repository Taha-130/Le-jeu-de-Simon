const slots = document.querySelectorAll(".slot");

const socket = new WebSocket("ws://" + location.host + "/ws/simon/" + code + "/");

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "players_update") {
        afficherJoueurs(data.players);
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