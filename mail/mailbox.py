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
        """Retourne le chemin du dossier de boite mail pour un destinataire.

        Le nom du dossier correspond a l'adresse email du destinataire.
        """
        dirname = recipient.replace("<", "").replace(">", "")
        return os.path.join(self.MAILBOX_DIR, dirname)

    def save_message(self, sender, recipient, data):
        """Sauvegarde un mail dans un fichier unique dans le dossier du destinataire.

        Cree le dossier s'il n'existe pas et incremente le nom du fichier.
        """
        directory = self.get_mailbox_path(recipient)
        if not os.path.exists(directory):
            os.makedirs(directory)

        clean_recipient = recipient.replace("<", "").replace(">", "")
        i = 1
        while True:
            filename = f"{i}_{clean_recipient}.txt"
            filepath = os.path.join(directory, filename)
            if not os.path.exists(filepath):
                break
            i += 1

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("From: " + sender + "\n")
            f.write("To: " + recipient + "\n")
            f.write("\n")
            f.write(data)
