
## X. Installation et Démarrage

### Prérequis

-   Un environnement Python 3.
    
-   Les ports 2525 (par défaut) ou 25 disponibles sur la machine.
    

### Lancement du serveur

Le point d'entrée du serveur se situe dans le script `server.py`.

Bash

```
# Lancement sur le port par défaut (2525)
python3 serveur/server.py

# Lancement sur un port spécifique
python3 serveur/server.py 8080

```

Dès le lancement, le dossier `mailboxes/` est automatiquement créé pour accueillir les futurs messages.

----------

## X. Guide d'Utilisation

### X.1 Connexion et Identification (Handshake)

Le serveur gère la phase d'identification conformément aux spécifications de la Version 2 :

1.  À la réception de `EHLO`, le serveur répond `502 Command not implemented` pour refuser les extensions.
    
2.  Le client doit alors utiliser `HELO`, auquel le serveur répond `250 OK`.
    

_Figure X : Séquence d'identification (Validation V2)_
[Insérer pour le rendu](https://github.com/PouletTendre/projet-smtp/blob/noah-sockets/uml/sequence_connexion_client.png)

### X.2 Envoi d'un courriel (Scénario Telnet)

Voici la procédure pour tester manuellement le serveur via un client Telnet :

1.  **Ouvrir la connexion** : `telnet localhost 2525`
    
2.  **S'identifier** : `HELO monclient`
    
3.  **Définir l'enveloppe** :
    
    -   `MAIL FROM:<moi@test.com>`
        
    -   `RCPT TO:<destinataire>`
        
4.  **Envoyer les données** :
    
    -   Commande `DATA`
        
    -   Saisir le sujet et le corps du message.
        
    -   Terminer par un point `.` seul sur une ligne.
        
5.  **Quitter** : `QUIT`
    

_Figure X : Diagramme de séquence pour l'envoi d'un mail_
[Insérer pour le rendu final](https://github.com/PouletTendre/projet-smtp/blob/noah-sockets/uml/sequence_envoi_mail.png)

### X.3 Utilisation avec Thunderbird


#### Étape 1 : Accéder aux Paramètres des Comptes

1.  Ouvrez Mozilla Thunderbird.
    
2.  Cliquez sur le menu (les trois lignes horizontales ≡) en haut à droite.
    
3.  Sélectionnez **Paramètres des comptes** (Account Settings).
    

#### Étape 2 : Ajouter le Serveur Sortant (SMTP)

Puisque notre projet (Version 2) ne gère que l'envoi (SMTP) et pas encore la réception (POP/IMAP est prévu pour la Version 3), nous allons configurer uniquement le serveur sortant.

1.  Dans la colonne de gauche, tout en bas, cliquez sur **Serveur sortant (SMTP)**.
    
2.  Cliquez sur le bouton **Ajouter...** à droite.
    
3.  Remplissez le formulaire avec les valeurs exactes correspondant à votre code source :
    
| **Champ** | **Valeur à saisir** | **Explication technique**  |
|--|--|--|
| **Description** | `Projet SMTP Local` |Nom libre pour vous repérer.|
| **Nom du serveur** |`127.0.0.1`  |L'adresse locale définie dans `server.py`.  |
| **Port** |`2525`  | Le port par défaut|
| **Sécurité de la connexion** |`Aucune`  |Notre `smtp_server.py` utilise une socket TCP simple sans SSL/TLS.  |
| **Méthode d'authentification** |`Pas d'authentification`  |Le `smtp_handler.py` ne gère pas la commande `AUTH`, seulement MAIL, RCPT, DATA.  |
| **Nom d'utilisateur** | (Laisser vide) | Non requis. |


4.  Cliquez sur **OK**.
    

#### Étape 3 : Associer ce serveur à une identité

Pour envoyer un mail, Thunderbird doit savoir quelle "identité" utilise ce serveur.

1.  Dans la liste des comptes à gauche, sélectionnez votre compte principal (ou un compte fictif si vous en avez créé un).
    
2.  Tout en bas de la page principale du compte, cherchez le champ **Serveur sortant (SMTP)**.
    
3.  Dans la liste déroulante, sélectionnez le serveur qu'on viens de créer : **Projet SMTP Local - 127.0.0.1**.
    

#### Étape 4 : Tester l'envoi

1.  Cliquez sur le bouton **Écrire** (Write) dans Thunderbird.
    
2.  **Expéditeur** : Assurez-vous que l'identité utilisant votre serveur local est sélectionnée.
    
3.  **Pour** : Mettez une adresse de test, par exemple `test@projet.fr`.
    
4.  **Sujet** : `Test Thunderbird V2`.
    
5.  **Corps** : `Ceci est un test depuis Thunderbird.`
    
6.  Cliquez sur **Envoyer**.
    

> **Note importante :** Il est possible que Thunderbird mette un peu de temps ou  avertisse que la connexion n'est pas chiffrée. Validez l'envoi.

#### Étape 5 : Vérification (Côté Serveur)

Si tout a fonctionné :

1.  **Dans votre terminal serveur**, vous devriez voir les logs de connexion :
    

    
    ```
    Connexion de ('127.0.0.1', xxxx)
    Fermeture connexion...
    
    ```
    
    _Thunderbird va d'abord tenter `EHLO`, recevoir votre erreur `502`, puis réessayer avec `HELO` et réussir._
    
2.  Dans les fichiers :
    
    Allez dans le dossier mailboxes à la racine de votre projet. Vous devriez trouver un fichier nommé test@projet.fr.txt (basé sur l'adresse du destinataire) contenant le message formaté.
    
----------
