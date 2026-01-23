
"""Point d'entree du client POP3.

Notre orchestrateur pour le client POP3.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.pop3_client import POP3Client


def main():
    """Lancement POP3"""
    host = "127.0.0.1"
    port = 1100

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    client = POP3Client(host, port)

    try:
        print("Connexion au serveur POP3...")
        response = client.connect()
        print("Serveur: " + response)

        user = input("\nUtilisateur (email): ")
        response = client.user(user)
        print("Serveur: " + response)

        if not response.startswith("+OK"):
            print("Erreur d'authentification")
            client.disconnect()
            return

        while True:
            print("\nCommandes disponibles:")
            print("1. STAT - Nombre de messages")
            print("2. LIST - Liste des messages")
            print("3. RETR - Lire un message")
            print("4. QUIT - Quitter")

            choix = input("\nChoix: ")

            if choix == "1":
                response = client.stat()
                print("Serveur: " + response)

            elif choix == "2":
                response = client.list_messages()
                print("Serveur:\n" + response)

            elif choix == "3":
                num = input("Numero du message: ")
                response = client.retr(int(num))
                print("Serveur:\n" + response)

            elif choix == "4":
                response = client.quit()
                print("Serveur: " + response)
                break

            else:
                print("Choix invalide")

    except ConnectionRefusedError:
        print("Erreur: Impossible de se connecter au serveur POP3")
    except KeyboardInterrupt:
        print("\nDeconnexion...")
        client.disconnect()


if __name__ == "__main__":
    main()
