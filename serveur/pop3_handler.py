"""Module de traitement des commandes POP3

Interprete les commandes POP3 envoyees par le client et retourne les reponses.
Commandes supportees : USER, QUIT, STAT, LIST, RETR
"""

from mail.mailbox import Mailbox


class POP3Handler:
    # Classe qui gere l'interpretation des commandes POP3


    def __init__(self):
        """Initialise le handler avec une boite mail."""
        self.mailbox = Mailbox()
        self.user = None

    def handle_command(self, line):
        # Identifie la commande et appelle la fonction correspondante.
        line = line.strip()
        if not line:
            return None

        parts = line.split()
        command = parts[0].upper()
        args = parts[1:] if len(parts) > 1 else []

        commands = {
            "USER": lambda: self.handle_user(args),
            "QUIT": self.handle_quit,
            "STAT": self.handle_stat,
            "LIST": lambda: self.handle_list(args),
            "RETR": lambda: self.handle_retr(args)
        }

        if command in commands:
            return commands[command]()
        return "-ERR Commande non reconnue" # si on se trompe

    def handle_user(self, args):
        # USER : Definit l'utilisateur dont on veut consulter la boite mail
        if len(args) < 1:
            return "-ERR Syntaxe: USER nom" # Utilisateur inconnue

        self.user = args[0]
        return "+OK Utilisateur " + self.user

    def handle_quit(self):
        # QUIT : Termine la session POP3
        return "+OK Serveur POP3 ferme la connexion"

    def handle_stat(self):
        # STAT : Retourne le nombre de messages et leur taille totale.
        if self.user is None:
            return "-ERR USER requis"

        count = self.mailbox.get_message_count(self.user)
        size = self.mailbox.get_total_size(self.user)
        return "+OK " + str(count) + " " + str(size)

    def handle_list(self, args):
        # LIST : Retourne la liste des messages.
        if self.user is None:
            return "-ERR USER requis"

        if len(args) > 0:
            msg_num = int(args[0])
            size = self.mailbox.get_message_size(self.user, msg_num)
            if size == 0:
                return "-ERR Message inexistant"
            return "+OK " + str(msg_num) + " " + str(size)

        count = self.mailbox.get_message_count(self.user)
        size = self.mailbox.get_total_size(self.user)
        response = "+OK " + str(count) + " messages (" + str(size) + " octets)\r\n"

        for i in range(1, count + 1):
            msg_size = self.mailbox.get_message_size(self.user, i)
            response += str(i) + " " + str(msg_size) + "\r\n"

        response += "."
        return response

    def handle_retr(self, args):
        """Traite la commande RETR.

        Retourne le contenu du message specifie.
        """
        if self.user is None:
            return "-ERR USER requis"

        if len(args) < 1:
            return "-ERR Syntaxe: RETR numero"

        msg_num = int(args[0])
        message = self.mailbox.get_message(self.user, msg_num)

        if message is None:
            return "-ERR Message inexistant"

        size = len(message.encode("utf-8"))
        response = "+OK " + str(size) + " octets\r\n"
        response += message + "\r\n"
        response += "."
        return response

    def is_quit(self, line):
        # Verification de la commande QUIT
        return line.strip().upper() == "QUIT"
