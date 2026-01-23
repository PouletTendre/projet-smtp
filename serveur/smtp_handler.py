"""Module de traitement des commandes SMTP.

Interprete les commandes envoyees par le client et retourne les reponses.
"""

from mail.mailbox import Mailbox


class SMTPHandler:
    # Classe qui gere l'interpretation des commandes SMTP.
    def __init__(self):
        """Initialise le handler avec une boite mail et reinitialise l'etat."""
        self.mailbox = Mailbox()
        self.sender = None
        self.recipient = None
        self.data_mode = False
        self.data_buffer = []

    def reset_state(self):
        # Reinitialise les variables de session.
        self.sender = None
        self.recipient = None
        self.data_mode = False
        self.data_buffer = []

    def handle_command(self, line):
        """Point d'entree principal pour traiter une commande

        Si on est en mode DATA, on traite le contenu du mail
        Sinon on identifie la commande et on appelle la fonction correspondante
        """
        if self.data_mode:
            return self.handle_data_content(line)

        line = line.strip()
        if not line:
            return None

        command = line.split()[0].upper()
        commands = {
            "HELO": lambda: self.handle_helo(line),
            "EHLO": self.handle_ehlo,
            "MAIL": lambda: self.handle_mail(line),
            "RCPT": lambda: self.handle_rcpt(line),
            "DATA": self.handle_data,
            "QUIT": lambda: "221 Au revoir"
        }

        if command in commands:
            return commands[command]()
        return "500 Commande non reconnue"

    def handle_helo(self, line):
        # Traite la commande HELO (identification du client en mode basique).
        # Verifie que le hostname est fourni.
        parts = line.split()
        if len(parts) < 2:
            return "501 Syntaxe: HELO hostname"
        return "250 OK"

    def handle_ehlo(self):
        """Traite la commande EHLO (identification du client en mode etendu).

        Retourne 502 car le mode etendu n'est pas supporte.
        """
        return "502 Command not implemented"

    def handle_mail(self, line):
        # MAIL FROM:<adresse>
        # Extrait l'adresse de l'expediteur et la stocke.
        upper_line = line.upper()
        if "FROM:" not in upper_line:
            return "501 Syntaxe: MAIL FROM:<adresse>"

        start = line.find("<")
        end = line.find(">")
        if start != -1 and end != -1:
            self.sender = line[start+1:end]
        else:
            parts = line.split(":")
            self.sender = parts[1].strip()
        return "250 OK"

    def handle_rcpt(self, line):
        # RCPT TO:<adresse>.
        # Extrait l'adresse du destinataire qui servira de nom de fichier.
        # Necessite que MAIL ait ete appele avant.
        if self.sender is None:
            return "503 MAIL requis avant RCPT"

        upper_line = line.upper()
        if "TO:" not in upper_line:
            return "501 Syntaxe: RCPT TO:<adresse>"

        start = line.find("<")
        end = line.find(">")
        if start != -1 and end != -1:
            self.recipient = line[start+1:end]
        else:
            parts = line.split(":")
            self.recipient = parts[1].strip()
        return "250 OK"

    def handle_data(self):
        # DATA
        # Active le mode reception du contenu du mail
        # Necessite que MAIL et RCPT aient ete appeles avant
  
        if self.sender is None:
            return "503 MAIL requis avant DATA"
        if self.recipient is None:
            return "503 RCPT requis avant DATA"

        self.data_mode = True
        self.data_buffer = []
        return "354 Entrez le message, terminez par FIN"

    def handle_data_content(self, line):
        """Traite chaque ligne du contenu du mail.

        Un point seul sur une ligne termine le mail et declenche la sauvegarde.
        Sinon la ligne est ajoutee au buffer.
        """
        if line.strip() == ".":
            self.data_mode = False
            data = "\n".join(self.data_buffer)
            self.mailbox.save_message(self.sender, self.recipient, data)
            self.reset_state()
            return "250 Message accepte"

        self.data_buffer.append(line.rstrip("\r\n"))
        return None

    def is_quit(self, line):
        """Verifie si la commande est QUIT.

        Utilisee par la session pour savoir quand fermer la connexion.
        """
        return line.strip().upper() == "QUIT"
