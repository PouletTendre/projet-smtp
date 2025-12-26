# Etape 1 : Projet SMTP

## Objectif

1. Établir le dialogue (La "Mainshake")

Ton code doit écouter sur un port (souvent le port 25 en local) et attendre qu'un client (comme un script Python ou un outil comme telnet) se connecte. Une fois connecté, le dialogue ressemble à un jeu de "question-réponse" textuel.
2. Gérer les trois commandes clés

Ton programme doit être capable d'interpréter les lignes de texte envoyées par le client et de réagir correctement :

    MAIL FROM:<expediteur@test.com>

        Ce que ça veut dire : C'est le signal de départ. Ton code doit simplement valider qu'il a reçu l'info et répondre au client avec un code de succès (généralement 250 OK).

    RCPT TO:<destinataire@exemple.fr>

        Ce que ça veut dire : C'est l'étape cruciale pour ton exercice. Ton code doit extraire l'adresse (ici destinataire@exemple.fr). C'est ce nom qui servira à nommer ton fichier de stockage.

    DATA

        Ce que ça veut dire : Le client annonce qu'il va envoyer le corps du mail. Ton code doit lire tout ce qui arrive ensuite jusqu'à ce qu'il voie une ligne contenant uniquement un point (.).

## Recrutement :

### Equipe 1 : Serveur

qu'est-ce qui caractérise un Serveur : Son port d'écoute RX et de transmission TX
Ce que dois faire un serveur : Ecouter(), comprendre(), traiter(), envoyer(), TERMINUS()

On a besoin d'un écouteur. Il n'est caractériser par son port d'écoute.
Ce qu'il fait : ecoute(), vérifie qu'on est bien quelqu'un qui nous parle. et si oui ou non ! remonter l'info.
Envoyer , caractériser par son port d'envoie
ce qu'il fait : envoyer(), au Mail l'info qu'il a reçu.

On a besoin d'un Cerveau. Son but, est d'activer les bonnes fonctions du serveurs quand on en a besoins.
Par exemple, au début on doit ecouter, comprendre, traiter, envoyer.
Ce qu'il caractérise : rien
ce qu'il fait : ce que le serveur doit faire, c'est le chef d'orchestre.

Comprendre : il doit comprendre chaque phrase qu'on lui envoie. 
Traiter : effectuer les actions qu'il a compris, par exemple, si on ecoute qu'un seul . on sait que c'est la fin
TERMINUS : Mets fin à la discussions en demander au client de stop et lui meme aussi de se stop.

### Equipe 2 : Client

qu'est-ce qui caractérise un Client : Son port d'ecoute et de transmissions
Ce que dois faire un client : Ecouter(), Ecrire(), Envoyer(), Cerveau(), Terminus(), traitement()

Quest'ce que caractérise le cerveau : rien
Son job : Executer des ordes pour que le client fonctionne, du style Ecouter, Ecrire, Envoyer.

Questce que caractérise l'écrivains : rien
Son job : Pouvoir écrire()

qu'est-ce qu'il caractérise le port d'écoute : Son port
son job : écouter ce qu'on lui dit

qu'est-ce qui caractérise l'envoie : son port d'émission
son job : envoyer() ce qu'on a ecrit.

qu'est-ce qui caractérise un traitement : la réponse de ce qu'on écoute. 
Son job : executer des ordres en fonction de ce qu'il recoit autorise ou pas l'écriture et autres....

Qu'est-ce qui caractérise terminus() : rien
son job : se tuer à la fin.

### Equipe 3 : mail

qu'est-ce qui caractérise un intermediaire : Son nom de fichier, nom du destinateur.
Ce que dois faire un Intermediaire : recevoir(), ce que Serveur lui envoie.
