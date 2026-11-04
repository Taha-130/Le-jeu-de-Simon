const statut = document.getElementById("statut");
const message = document.getElementById("message");
const boutonRouge = document.getElementById("bouton-rouge");

const socket = new WebSocket("ws://127.0.0.1:8000/ws/simon/");

socket.onopen = function () {
    statut.textContent = "WebSocket connecté";
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    message.textContent = data.message;
};

socket.onclose = function () {
    statut.textContent = "WebSocket déconnecté";
};

boutonRouge.addEventListener("click", function () {
    socket.send(JSON.stringify({
        couleur: "rouge"
    }));
});