"""
Module de gestion des emails.
Contient la classe Email pour représenter et sauvegarder les emails.
"""

import os


class Email:
    """
    Classe modèle représentant un e-mail.
    Contient les informations de l'e-mail et la logique pour le sauvegarder.
    """

    def __init__(self):
        """Initialise un email vide."""
        self.expediteur = ""
        self.destinataire = ""
        self.contenu = ""

    def get_expediteur(self) -> str:
        """Retourne l'adresse de l'expéditeur."""
        return self.expediteur

    def set_expediteur(self, expediteur: str):
        """Définit l'adresse de l'expéditeur."""
        self.expediteur = expediteur

    def get_destinataire(self) -> str:
        """Retourne l'adresse du destinataire."""
        return self.destinataire

    def set_destinataire(self, destinataire: str):
        """Définit l'adresse du destinataire."""
        self.destinataire = destinataire

    def get_contenu(self) -> str:
        """Retourne le contenu du mail."""
        return self.contenu

    def set_contenu(self, contenu: str):
        """Définit le contenu du mail."""
        self.contenu = contenu

    def sauvegarder(self, repertoire: str = "mailboxes"):
        """
        Sauvegarde l'e-mail dans un fichier texte.
        Le nom du fichier est basé sur l'adresse du destinataire.
        
        :param repertoire: Le répertoire où sauvegarder les emails (par défaut: 'mailboxes')
        """
        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(repertoire):
            os.makedirs(repertoire)
        
        # Créer un nom de fichier valide à partir de l'adresse e-mail
        nom_fichier = self.destinataire.replace('@', '_').replace('.', '_') + ".txt"
        chemin_complet = os.path.join(repertoire, nom_fichier)
        
        try:
            with open(chemin_complet, 'a', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"From: <{self.expediteur}>\n")
                f.write(f"To: <{self.destinataire}>\n")
                f.write("\n")  # Ligne vide pour séparer les en-têtes du corps
                f.write(self.contenu)
                f.write("\n" + "=" * 50 + "\n\n")
            print(f"E-mail sauvegardé dans le fichier : {chemin_complet}")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde de l'e-mail : {e}")
