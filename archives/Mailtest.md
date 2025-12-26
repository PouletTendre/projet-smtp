## Equipe 1 : Serveur

**Attributs :** Port d'écoute (ex: 25), Socket principale.
**Rôle :** Attendre les connexions et déléguer le travail.

#### Sous-composant : Le "ClientHandler" (Le Cerveau par connexion)
Une fois qu'un client est connecté, ce gestionnaire prend le relais.
**Attributs :** La socket du client connecté, l'état actuel (a-t-on reçu le MAIL FROM ?).
**Méthodes :**
1.  `recevoir_commande()` : Lit ce que le client envoie (l'oreille).
2.  `analyser_commande()` : Comprend (Est-ce MAIL FROM ? RCPT TO ? DATA ?).
3.  `repondre()` : Envoie le code (250 OK, 354 Start mail input, etc.) (la bouche).
4.  `sauvegarder_mail()` : Si tout est fini, écrit le fichier sur le disque.

## Equipe 2 : Client
**Attributs :** Adresse du serveur cible, Port cible, Socket.
**Rôle :** Chef d'orchestre qui instancie les étapes une par une.

#### Les Spécialistes (Sous-classes par étape)
Chaque classe prend la **Socket** en paramètre pour pouvoir parler.

1.  **Classe `EtapeEmetteur`**
    *   Action : Envoie `MAIL FROM:<expediteur>`
    *   Vérification : Attend code 250.
2.  **Classe `EtapeRecepteur`**
    *   Action : Envoie `RCPT TO:<destinataire>`
    *   Vérification : Attend code 250.
3.  **Classe `EtapeDonnees`**
    *   Action : Envoie `DATA`
    *   Vérification : Attend code 354.
4.  **Classe `EtapeCorps` (Finalité)**
    *   Action : Envoie le texte + `.` seul sur une ligne.
    *   Vérification : Attend code 250.
5.  **Classe `EtapeTerminus`**
    *   Action : Envoie `QUIT`.
    *   Vérification : Ferme la connexion.


## Equipe 3 : mail
**Nature :** Un objet de données (passif).
**Attributs :**
- `expediteur` (str)
- `destinataire` (str)
- `contenu` (str)
**Méthode :** `__str__()` pour se formater proprement avant l'écriture dans un fichier.



## Architecture des Fichiers
projet-smtp/
│
├── mail.py              # (Le Modèle) L'objet Mail passif
│
├── server.py            # (Le Serveur Main) Lance l'écoute
├── server_handler.py    # (Le Cerveau Serveur) La classe ClientHandler
│
├── client.py            # (Le Client Main) Interaction utilisateur
└── client_steps.py      # (Les Outils Client) Les classes Etape...


Organisation recommandée du code source :

1.  **`mail.py`** (Modèle)
    *   Contient la classe `Mail`.
    *   Utilisé par le serveur pour stocker les infos avant la sauvegarde.

2.  **`server_handler.py`** (Logique Serveur)
    *   Contient la classe `ClientHandler`.
    *   Gère la conversation (`recevoir`, `analyser`, `repondre`).

3.  **`server.py`** (Main Serveur)
    *   Crée la socket d'écoute et accepte les connexions.
    *   Instancie `ClientHandler` pour chaque client.

4.  **`client_steps.py`** (Logique Client)
    *   Contient les classes `EtapeEmetteur`, `EtapeRecepteur`, etc.

5.  **`client.py`** (Main Client)
    *   Gère les `input()` utilisateur.
    *   Instancie la socket et appelle les étapes de `client_steps.py`.
