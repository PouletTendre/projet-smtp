"""Module du serveur POP3.

Gere la socket d'ecoute et accepte les connexions entrantes pour POP3.
"""

import socket
from serveur.pop3_session import POP3Session


class POP3Server:
    # Classe principale du serveur POP3

    def __init__(self, host, port):
        """Initialise le serveur avec l'adresse et le port"""
        self.host = host
        self.port = port
        self.socket_ecoute = None
        self.running = False

    def start(self):
        """Demarre le serveur POP3

        Cree la socket d'ecoute et attend les connexions
        Pour chaque client, cree une nouvelle session
        """
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_ecoute.bind((self.host, self.port))
        self.socket_ecoute.listen(5)
        self.running = True

        print("Serveur POP3 demarre sur le port " + str(self.port) + "...")
        print("En attente de connexions...")

        while self.running:
            try:
                client_socket, client_address = self.socket_ecoute.accept()
                session = POP3Session(client_socket, client_address)
                session.start()
            except KeyboardInterrupt:
                print("Arret du serveur POP3 demande par l'utilisateur...")
                self.stop()
            except OSError as e:
                print("Erreur serveur POP3: " + str(e))

    def stop(self):
        # STOP le serveur et la socket d'écoute
        self.running = False
        if self.socket_ecoute:
            self.socket_ecoute.close()
        print("Serveur POP3 arrete.")
