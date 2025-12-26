# Projet SMTP

## PROJET UNIVERSITAIRE

Implémentation d'un serveur SMTP et d'un client en Python pour l'envoi et la réception d'emails.

## Structure du projet

```
projet-smtp/
├── client/                 # Module client SMTP
│   ├── client.py          # Interface utilisateur du client
│   └── client_functions.py # Fonctions de communication SMTP
├── serveur/               # Module serveur SMTP
│   ├── server.py          # Point d'entrée du serveur
│   └── server_functions.py # Gestionnaire de clients
├── mail/                  # Module de gestion des emails
│   └── mail.py            # Classe Email pour modéliser les messages
├── mailboxes/             # Boîtes aux lettres (créé automatiquement)
└── archives/              # Code de référence
```

## Installation et lancement

### Prérequis
- Python 3.6 ou supérieur
- Aucune dépendance externe nécessaire

### Démarrer le serveur

```bash
cd serveur
python server.py <port>
```

Exemple :
```bash
python server.py 2525
```

### Utiliser le client

Dans un autre terminal :
```bash
cd client
python client.py
```

Ou avec les paramètres en ligne de commande :
```bash
python client.py <host> <port>
```

Exemple :
```bash
python client.py localhost 2525
```

## Fonctionnalités

### Version 1 (Actuelle) - SMTP Simple ✅
- Commande `MAIL FROM` : Spécifier l'expéditeur
- Commande `RCPT TO` : Spécifier le destinataire
- Commande `DATA` : Envoyer le contenu du message
- Commande `QUIT` : Fermer la connexion
- Sauvegarde des emails dans des fichiers (boîtes aux lettres)

### Version 2 (À venir) - HELO/EHLO
- Gestion de l'identification du protocole
- Compatibilité avec clients standards (Thunderbird, etc.)

### Version 3 (À venir) - POP3
- Consultation à distance des emails
- Commandes STAT, LIST, RETR, QUIT

## Utilisation

### Mode interactif
1. Lancer le serveur
2. Lancer le client
3. Choisir l'option 1 pour envoyer un email
4. Saisir les informations demandées
5. Taper "FIN" pour terminer le message

### Mode automatique
- Choisir l'option 2 pour envoyer un email de test

### Test avec telnet

Vous pouvez aussi tester le serveur avec telnet :

```bash
telnet localhost 2525
```

Puis taper les commandes SMTP :
```
MAIL FROM:<expediteur@example.com>
RCPT TO:<destinataire@example.com>
DATA
Sujet: Test
Contenu du message
.
QUIT
```

## Codes de réponse SMTP

- `220` : Service prêt
- `250` : Commande acceptée
- `354` : Début de saisie du message
- `221` : Fermeture de connexion
- `501` : Erreur de syntaxe
- `502` : Commande non implémentée

## Auteurs

M1 R&T / 2A STRI - Projet Déploiement de Services et Interopérabilité
