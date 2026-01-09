"""Module du serveur SMTP.

Gere la socket d'ecoute et accepte les connexions entrantes.
"""

import socket
from serveur.smtp_session import SMTPSession


class SMTPServer:
    """Classe principale du serveur SMTP.

    Cree une socket d'ecoute TCP et gere les connexions clients.
    """

    def __init__(self, host, port):
        """Initialise le serveur avec l'adresse et le port d'ecoute."""
        self.host = host
        self.port = port
        self.socket_ecoute = None
        self.running = False

    def start(self):
        """Demarre le serveur SMTP.

        Cree la socket d'ecoute et attend les connexions.
        Pour chaque client, cree une nouvelle session.
        """
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_ecoute.bind((self.host, self.port))
        self.socket_ecoute.listen(5)
        self.running = True

        print("Serveur SMTP demarre sur le port " + str(self.port) + "...")
        print("En attente de connexions...")

        while self.running:
            try:
                client_socket, client_address = self.socket_ecoute.accept()
                session = SMTPSession(client_socket, client_address)
                session.start()
            except KeyboardInterrupt:
                print("Arret du serveur demande par l'utilisateur...")
                self.stop()
            except OSError as e:
                print("Erreur serveur: " + str(e))

    def stop(self):
        """Arrete le serveur et ferme la socket d'ecoute."""
        self.running = False
        if self.socket_ecoute:
            self.socket_ecoute.close()
        print("Serveur arrete.")
