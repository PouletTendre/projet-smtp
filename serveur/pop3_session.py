"""Module de gestion des sessions POP3.

Gere la communication avec un client POP3 connecte.
"""

from serveur.pop3_handler import POP3Handler


class POP3Session:
    """Classe qui gere une session avec un client POP3.

    Recoit les commandes, les transmet au handler et renvoie les reponses.
    """

    def __init__(self, client_socket, client_address):
        """Initialise la session avec la socket client et son adresse."""
        self.client_socket = client_socket
        self.client_address = client_address
        self.handler = POP3Handler()
        self.running = True
        self.buffer = ""

    def start(self):
        """Demarre la session et boucle sur la reception des commandes.

        Envoie d'abord le message de bienvenue.
        Puis traite chaque ligne recue jusqu'a QUIT ou deconnexion.
        """
        print("Connexion POP3 de " + str(self.client_address))
        self.send_response("+OK Serveur POP3 pret")

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
                print("Erreur decodage POP3: " + str(e))
                break
            except ConnectionError as e:
                print("Erreur connexion POP3: " + str(e))
                break

        self.close()

    def send_response(self, response):
        """Envoie une reponse au client avec un retour a la ligne."""
        message = response + "\r\n"
        self.client_socket.send(message.encode("utf-8"))

    def close(self):
        """Ferme la connexion avec le client."""
        print("Fermeture connexion POP3 " + str(self.client_address))
        self.client_socket.close()
