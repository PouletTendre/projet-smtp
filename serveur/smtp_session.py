"""Module de gestion des sessions SMTP.

Gere la communication avec un client connecte.
"""

from serveur.smtp_handler import SMTPHandler


class SMTPSession:
    """Classe qui gere une session avec un client SMTP.
    Recoit les commandes, les transmet au handler et renvoie les reponses.
    """

    def __init__(self, client_socket, client_address):
        """Initialise la session avec la socket client et son adresse."""
        self.client_socket = client_socket
        self.client_address = client_address
        self.handler = SMTPHandler()
        self.running = True
        self.buffer = ""

    def start(self):
        """Demarre la session et boucle sur la reception des commandes
        Envoie d'abord le message de bienvenue 220
        Puis traite chaque ligne recue jusqu'a QUIT ou deconnexion
        """
        print("Connexion de " + str(self.client_address))
        self.send_response("220 Serveur SMTP pret")

        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                self.buffer += data.decode("utf-8")

                while "\r\n" in self.buffer or "\n" in self.buffer:
                    if "\r\n" in self.buffer:
                        line, self.buffer = self.buffer.split("\r\n", 1)
                    else:
                        line, self.buffer = self.buffer.split("\n", 1)

                    response = self.handler.handle_command(line)

                    if response is not None:
                        self.send_response(response)

                    if self.handler.is_quit(line):
                        self.running = False
                        break

            except UnicodeDecodeError as e:
                print("Erreur decodage: " + str(e))
                break
            except ConnectionError as e:
                print("Erreur connexion: " + str(e))
                break

        self.close()

    def send_response(self, response):
        """Envoie une reponse au client avec un retour a la ligne."""
        message = response + "\r\n"
        self.client_socket.send(message.encode("utf-8"))

    def close(self):
        """Ferme la connexion avec le client."""
        print("Fermeture connexion " + str(self.client_address))
        self.client_socket.close()
