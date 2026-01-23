"""Point d'entree du client SMTP.

Permet d'envoyer un mail de maniere interactive.
Utilisation : python client.py [port]
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from client.smtp_client import SMTPClient


def main():
    """Debut du programme : laisse le choix à l'utilisateur de faire ce qu'il souhaite
    """
    host = "127.0.0.1"
    port = 2525

    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    client = SMTPClient(host, port)

    try:
        print("Connexion au serveur SMTP...")
        response = client.connect()
        print("Serveur: " + response)

        print("\nEnvoi d'un mail de test...")

        sender = input("Expediteur: ")
        recipient = input("Destinataire: ")
        subject = input("Sujet: ")
        print("Corps du message (terminez par FIN sur une ligne):")

        body_lines = []
        while True:
            line = input()
            if line == "FIN":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

        success = client.send_mail(sender, recipient, subject, body)

        if success:
            print("Mail envoye avec succes.")
        else:
            print("Erreur lors de l'envoi du mail.")

        client.quit()

    except ConnectionError as e:
        print("Erreur connexion: " + str(e))
        client.close()
    except OSError as e:
        print("Erreur: " + str(e))
        client.close()


if __name__ == "__main__":
    main()
