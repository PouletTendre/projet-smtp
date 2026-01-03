"""Module de gestion des boites mail.

Permet de stocker les mails recus dans des fichiers.
"""

import os


class Mailbox:
    """Classe qui gere le stockage des mails dans des fichiers texte.

    Chaque destinataire a son propre fichier dans le dossier mailboxes/
    """

    MAILBOX_DIR = "mailboxes"

    def __init__(self):
        """Cree le dossier mailboxes s'il n'existe pas."""
        if not os.path.exists(self.MAILBOX_DIR):
            os.makedirs(self.MAILBOX_DIR)

    def get_mailbox_path(self, recipient):
        """Retourne le chemin du fichier de boite mail pour un destinataire.

        Le nom du fichier correspond a l'adresse email du destinataire.
        """
        filename = recipient.replace("<", "").replace(">", "")
        return os.path.join(self.MAILBOX_DIR, filename + ".txt")

    def save_message(self, sender, recipient, data):
        """Sauvegarde un mail dans le fichier du destinataire.

        Ajoute les en-tetes From et To puis le contenu du message.
        """
        path = self.get_mailbox_path(recipient)
        with open(path, "a", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("From: " + sender + "\n")
            f.write("To: " + recipient + "\n")
            f.write("\n")
            f.write(data)
            f.write("\n")
