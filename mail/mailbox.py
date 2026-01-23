# Gestionnaire de fichier

import os


class Mailbox:
    """Classe qui gere le stockage des mails dans des fichiers texte

    Chaque destinataire a son propre fichier dans le dossier mailboxes/
    """

    MESSAGE_SEPARATOR = "=" * 50

    def __init__(self):
        # Cree le dossier mailboxes s'il n'existe pas.
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mailbox_dir = os.path.join(base_dir, "mailboxes")
        if not os.path.exists(self.mailbox_dir):
            os.makedirs(self.mailbox_dir)

    def get_mailbox_path(self, recipient):
        """Retourne le chemin du fichier de boite mail pour un destinataire
        Le nom du fichier correspond a l'adresse email du destinataire
        """
        filename = recipient.replace("<", "").replace(">", "")
        return os.path.join(self.mailbox_dir, filename + ".txt")

    def save_message(self, sender, recipient, data):
        """Sauvegarde un mail dans le fichier du destinataire

        Ajoute les en-tetes From et To puis le contenu du message
        """
        path = self.get_mailbox_path(recipient)
        with open(path, "a", encoding="utf-8") as f:
            f.write(self.MESSAGE_SEPARATOR + "\n")
            f.write("From: " + sender + "\n")
            f.write("To: " + recipient + "\n")
            f.write("\n")
            f.write(data)
            f.write("\n")

    def get_messages(self, user):
        """Retourne la liste des messages pour un utilisateur

        Chaque message est une chaine de caracteres
        """
        path = self.get_mailbox_path(user)
        if not os.path.exists(path):
            return []

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            return []

        parts = content.split(self.MESSAGE_SEPARATOR + "\n")
        messages = []
        for part in parts:
            if part.strip():
                messages.append(part.strip())

        return messages

    def get_message_count(self, user):
        # Retourne le nombre de messages pour 1 utilisateur
        return len(self.get_messages(user))

    def get_total_size(self, user):
        # Retourne la taille totale en octets des messages
        messages = self.get_messages(user)
        total = 0
        for msg in messages:
            total += len(msg.encode("utf-8"))
        return total

    def get_message(self, user, msg_num):
        # Retourne un message par son numero (1-indexed)
        messages = self.get_messages(user)
        if msg_num < 1 or msg_num > len(messages):
            return None # Retourne None si le message n'existe pas
        return messages[msg_num - 1]

    def get_message_size(self, user, msg_num):
        # Retourne la taille d'un message en octets
        msg = self.get_message(user, msg_num)
        if msg is None:
            return 0
        return len(msg.encode("utf-8"))
