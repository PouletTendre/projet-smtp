"""Module client POP3.

Permet de se connecter a un serveur POP3 et de consulter les mails.
"""

import socket


class POP3Client:
    """Classe client pour le protocole POP3."""

    def __init__(self, host, port):
        """Initialisation"""
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        # Connection au serveur POP3Client --> Serveur
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self.receive()

    def send(self, command):
        # Envoie une commande au serveur. 
        self.socket.send((command + "\r\n").encode("utf-8"))

    def receive(self):
        # Recoit une reponse du serveur. Retourne la reponse decodee.
        data = self.socket.recv(4096)
        return data.decode("utf-8").strip()

    def user(self, username):
        # Commande USER
        self.send("USER " + username)
        return self.receive()

    def stat(self):
        # Commande STAT
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
        # Commande RETR et son contenue
        self.send("RETR " + str(msg_num))
        return self.receive()

    def quit(self):
        # Envoie la commande QUIT et ferme la connexion
        self.send("QUIT")
        response = self.receive()
        self.socket.close()
        return response

    def disconnect(self):
        # Rupture brutal
        if self.socket:
            self.socket.close()
