"""Module client POP3.

Permet de se connecter a un serveur POP3 et de consulter les mails.
"""

import socket


class POP3Client:
    """Classe client pour le protocole POP3.

    Gere la connexion et l'envoi de commandes au serveur POP3.
    """

    def __init__(self, host, port):
        """Initialise le client avec l'adresse et le port du serveur."""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        """Se connecte au serveur POP3.

        Retourne le message de bienvenue du serveur.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self.receive()

    def send(self, command):
        """Envoie une commande au serveur.

        Ajoute automatiquement le retour a la ligne.
        """
        self.socket.send((command + "\r\n").encode("utf-8"))

    def receive(self):
        """Recoit une reponse du serveur.

        Retourne la reponse decodee.
        """
        data = self.socket.recv(4096)
        return data.decode("utf-8").strip()

    def user(self, username):
        """Envoie la commande USER.

        Retourne la reponse du serveur.
        """
        self.send("USER " + username)
        return self.receive()

    def stat(self):
        """Envoie la commande STAT.

        Retourne le nombre de messages et la taille totale.
        """
        self.send("STAT")
        return self.receive()

    def list_messages(self, msg_num=None):
        """Envoie la commande LIST.

        Sans argument : liste tous les messages.
        Avec argument : info sur un message specifique.
        """
        if msg_num:
            self.send("LIST " + str(msg_num))
        else:
            self.send("LIST")
        return self.receive()

    def retr(self, msg_num):
        """Envoie la commande RETR.

        Retourne le contenu du message specifie.
        """
        self.send("RETR " + str(msg_num))
        return self.receive()

    def quit(self):
        """Envoie la commande QUIT et ferme la connexion."""
        self.send("QUIT")
        response = self.receive()
        self.socket.close()
        return response

    def disconnect(self):
        """Ferme la connexion si elle est ouverte."""
        if self.socket:
            self.socket.close()
