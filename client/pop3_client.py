import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=wrong-import-position
from client.pop3_protocol import POP3Client


def main():
    """Fonction principale qui lance le client POP3 en mode interactif.

    Authentifie l'utilisateur et permet de lire ses mails.
    """
    host = "127.0.0.1"
    port = 110

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    client = POP3Client(host, port)

    try:
        print("Connexion au serveur POP3...")
        response = client.connect()
        print("Serveur: " + response)

        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")

        success, msg = client.authenticate(username, password)
        print("Serveur: " + msg)
        
        if not success:
            client.quit()
            return

        print("\nListe des messages:")
        listing = client.list_messages()
        if listing is not None:
            print(listing)
        else:
            print("Erreur lors du listing.")

        while True:
            choice = input("\nEntrez le numero du message a lire (ou QUIT pour quitter): ")
            if choice.upper() == "QUIT":
                break
            
            content = client.retrieve_message(choice)
            if content:
                print("\n--- Debut du message ---")
                print(content)
                print("--- Fin du message ---")
            else:
                print("Erreur ou message introuvable.")

        client.quit()

    except ConnectionError as e:
        print("Erreur connexion: " + str(e))
        client.close()
    except OSError as e:
        print("Erreur: " + str(e))
        client.close()


if __name__ == "__main__":
    main()
