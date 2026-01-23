"""Module client SMTP

Permet d'envoyer des mails via le protocole SMTP
"""

import socket


class SMTPClient:
    """Classe client pour envoyer des mails a un serveur SMTP
    Gere la connexion, l'envoi des commandes et la reception des reponses
    """

    def __init__(self, host, port):
        """Initialisation..."""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False

    def connect(self):
        """Etablissement de la connexion
        Si ok : retourne le message de bienvenue du serveur
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connected = True
        response = self.receive()
        return response

    def send_command(self, command):
        """Client --> serveur"""
        if not self.connected:
            return None
        message = command + "\r\n"
        self.socket.send(message.encode("utf-8"))
        response = self.receive()
        return response

    def receive(self):
        """Serveur <--- Client"""
        data = self.socket.recv(1024)
        return data.decode("utf-8").strip()

    def send_mail(self, sender, recipient, subject, body):
        """Envoie un mail complet au serveur.
        """
        self.send_command("HELO localhost")
        
        #Emmeteur
        response = self.send_command("MAIL FROM:<" + sender + ">")
        if not response.startswith("250"):
            return False

        #Recepteur
        response = self.send_command("RCPT TO:<" + recipient + ">")
        if not response.startswith("250"):
            return False

        #Données
        response = self.send_command("DATA")
        if not response.startswith("354"):
            return False

        message = "Subject: " + subject + "\r\n"
        message += "\r\n"
        message += body + "\r\n"
        message += "."

        response = self.send_command(message)
        if not response.startswith("250"):
            return False

        return True

    # Deconnexion
    def quit(self):
        """Envoie QUIT et ferme la connexion proprement"""
        if self.connected:
            self.send_command("QUIT")
            self.socket.close()
            self.connected = False

    # Rupture brut de la connexion
    def close(self):
        """Ferme la connexion sans envoyer QUIT"""
        if self.socket:
            self.socket.close()
            self.connected = False
