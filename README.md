# Le-jeu-de-Simon

Cahier des charges - Projet FISA 2A “Simon Online”
Kévin PETIT (BUT), Mattéo RIQUE (Prépa), Taha SEFOUDINE (BUT)


Contexte et définition du projet :

Nous devons réaliser un projet informatique intégrant une composante visuelle et une composante réseau. Pour répondre à ces besoins, nous avons choisi de développer un jeu web multijoueur de Simon en ligne. Le concept du Simon y est modifié pour intégrer une mécanique similaire au jeu du “Dans ma valise” pour créer une mécanique de compétition multijoueur tour par tour.


Objectifs du projet : 

Implémenter un site web capable de gérer des salons virtuels stables accueillant jusqu’à 4 joueurs simultanés
Déployer un mode de jeu fonctionnel avec gestion des tours, du chronomètre et des éliminations


Périmètre du projet : 

Inclus dans le projet : 
Développement de l’interface visuelle reprenant les 4 boutons colorés du Simon classique (rouge, bleu, vert, jaune)
Développement du serveur web pour la gestion du multijoueur (proposition de Django complété par une technologie temps réel comme WebSockets par exemple)
Création d’un système de salon permettant de regrouper 4 joueurs maximum avant le lancement d’une partie

Exclus du projet : 
Création de comptes utilisateurs persistants (pseudos temporaires uniquement)
Adaptation de l’affichage pour les terminaux mobiles (interface web prévue pour PC) 


Description fonctionnelle du besoin : 

Création de partie : un joueur crée un salon de maximum 4 joueurs et invite d’autres joueurs, pas de possibilité de rejoindre en cours de partie
Boucle de jeu : le joueur 1 initie la séquence en cliquant sur une couleur, le joueur 2 doit reproduire cette couleur et en ajouter une nouvelle à la fin de la séquence, le joueur 3 doit reproduire les deux couleurs précédentes et en ajouter une nouvelle, et ainsi de suite…
Chronomètre : chaque joueur dispose d’un temps limité pour reproduire la dernière séquence
Élimination : si un joueur ne reproduit pas correctement la séquence ou que son temps est écoulé, il est éliminé et devient spectateur. La séquence ne repart pas à zéro, le joueur suivant doit reproduire la séquence ratée par le joueur précédent avant de pouvoir ajouter à son tour une nouvelle couleur à la séquence
Fin de partie : le jeu continue jusqu’à ce qu’il ne reste plus qu’un joueur, qui remporte alors la partie


Enveloppe budgétaire et ressources : 

Ressources humaines : équipe de 3 étudiants développeurs
Ressources matérielles et logicielles : outils de développement open-source (Django mentionné précédemment) et un serveur hôte (budget estimé entre 0€ - 10€ pour des solutions d’hébergement suffisantes)


Délais : 

Temps de développement : 10 séances de 3h, 30h/personne de développement (incluant également la phase de planification du projet)
Deadline : décembre 2026




