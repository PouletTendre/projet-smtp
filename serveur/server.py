"""
Serveur SMTP principal.
Lance le serveur et accepte les connexions clientes.
"""

import socket
import threading
import sys
from server_functions import GestionnaireClient


class ServeurSMTP:
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

            print(f"🚀 Serveur SMTP démarré sur le port {self.port}...")
            print("En attente de connexions...")

            while True:
                try:
                    # Attendre une nouvelle connexion cliente
                    client_socket, addr = self.server_socket.accept()
                    print(f"✅ Nouveau client connecté : {addr}")

                    # Déléguer la gestion du client à un nouveau thread
                    gestionnaire = GestionnaireClient(client_socket)
                    client_thread = threading.Thread(target=gestionnaire.run)
                    client_thread.daemon = True  # Le thread se ferme avec le programme principal
                    client_thread.start()

                except IOError as e:
                    print(f"❌ Erreur lors de l'acceptation de la connexion client : {e}")

        except OSError as e:
            print(f"❌ Impossible de démarrer le serveur sur le port {self.port} : {e}")
        except KeyboardInterrupt:
            print("\n⚠️  Arrêt du serveur demandé par l'utilisateur...")
        finally:
            if self.server_socket:
                self.server_socket.close()
                print("🛑 Serveur arrêté.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        print("Exemple: python server.py 2525")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        if port < 1024 or port > 65535:
            print("⚠️  Attention : Il est recommandé d'utiliser un port entre 1024 et 65535")
        
        serveur = ServeurSMTP(port)
        serveur.demarrer()
    except ValueError:
        print("❌ Erreur : Le port doit être un nombre entier.")
        sys.exit(1)
