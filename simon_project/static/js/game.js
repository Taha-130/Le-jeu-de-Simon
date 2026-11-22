const joueursDiv = document.getElementById("joueurs");
const info = document.getElementById("info");
const alerte = document.getElementById("alerte");
const plateau = document.getElementById("plateau");
const retour = document.getElementById("retour");
const chargement = document.getElementById("chargement");
const boutonsCouleur = document.querySelectorAll(".simon");

setTimeout(function () {
    chargement.classList.add("d-none");
}, 3000);

const socket = new WebSocket("ws://" + location.host + "/ws/simon/" + code + "/");

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    if (data.type === "state") {
        afficherEtat(data);
    }
    if (data.type === "color_played") {
        allumer(data.color);
        if (data.wrong) {
            alerte.textContent = data.player + " s'est trompé (" + data.color + ") et est éliminé !";
        } else {
            alerte.textContent = data.player + " a joué " + data.color;
        }
    }
    if (data.type === "error") {
        alerte.textContent = data.message;
    }
};

boutonsCouleur.forEach(function (bouton) {
    bouton.addEventListener("click", function () {
        socket.send(JSON.stringify({ type: "color", color: bouton.dataset.color }));
    });
});

function afficherEtat(data) {
    joueursDiv.innerHTML = "";
    data.players.forEach(function (p) {
        const carte = document.createElement("div");
        carte.className = "slot plein";
        if (p.eliminated) carte.classList.add("elimine");
        if (p.name === data.current && !data.winner) carte.classList.add("actif");
        carte.textContent = p.name;
        joueursDiv.appendChild(carte);
    });

    const moiJoueur = data.players.find(function (p) { return p.name === moi; });

    plateau.classList.add("inactif");

    if (data.winner) {
        info.textContent = data.winner === moi ? "Tu as gagné !" : data.winner + " a gagné la partie !";
        retour.classList.remove("d-none");
    } else if (moiJoueur && moiJoueur.eliminated) {
        info.textContent = "Tu es éliminé, tu regardes la fin de la partie.";
    } else if (data.current === moi) {
        plateau.classList.remove("inactif");
        info.textContent = "À toi de jouer ! (" + data.length + " couleur(s) à reproduire)";
    } else {
        info.textContent = "C'est à " + data.current + " de jouer.";
    }
}

function allumer(couleur) {
    const bouton = document.querySelector(".simon." + couleur);
    bouton.classList.add("allume");
    setTimeout(function () {
        bouton.classList.remove("allume");
    }, 800);
}