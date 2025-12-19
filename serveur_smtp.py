import socket
import threading
from gestionnaire_client import GestionnaireClient


class ServeurSmtp:
    """
    Classe principale du serveur SMTP.
    Elle est responsable d'accepter les connexions clientes et de déléguer leur traitement.
    """


    def __init__(self, port: int):
        """
        Constructeur du serveur SMTP.
        :param port: Le port d'écoute du serveur.
        """
        self.port = port
        self.server_socket = None


    def demarrer(self):
        """
        Démarre le serveur. Le serveur écoute en boucle les connexions entrantes
        et crée un nouveau GestionnaireClient pour chaque client connecté.
        """
        try:
            # Création du socket TCP/IP
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permet de réutiliser l'adresse immédiatement après l'arrêt du serveur
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.port))
            self.server_socket.listen(5)  # Jusqu'à 5 connexions en attente


            print(f"Serveur SMTP démarré sur le port {self.port}...")


            while True:
                try:
                    # Attendre une nouvelle connexion cliente
                    client_socket, addr = self.server_socket.accept()
                    print(f"Nouveau client connecté : {addr}")


                    # Déléguer la gestion du client à un nouveau thread
                    gestionnaire = GestionnaireClient(client_socket)
                    client_thread = threading.Thread(target=gestionnaire.run)
                    client_thread.start()


                except IOError as e:
                    print(f"Erreur lors de l'acceptation de la connexion client : {e}")


        except OSError as e:
            print(f"Impossible de démarrer le serveur sur le port {self.port} : {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 serveur_smtp.py <port>")
        sys.exit(1)


    try:
        port = int(sys.argv[1])
        serveur = ServeurSmtp(port)
        serveur.demarrer()
    except ValueError:
        print("Erreur : Le port doit être un nombre entier.")
        sys.exit(1)