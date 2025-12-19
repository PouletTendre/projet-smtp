import os


class Email:
    """
    Le Formulaire (Modèle) : C'est l'objet qui va contenir toutes les données du mail.
    Classe modèle représentant un e-mail.
    Contient les informations de l'e-mail et la logique pour le sauvegarder.
    """


    # De base, tt est vide !
    def __init__(self):
        self.expediteur = ""
        self.destinataire = ""
        self.contenu = ""


    # Getters et Setters
    def get_expediteur(self) -> str:
        return self.expediteur


    def set_expediteur(self, expediteur: str):
        self.expediteur = expediteur


    def get_destinataire(self) -> str:
        return self.destinataire


    def set_destinataire(self, destinataire: str):
        self.destinataire = destinataire


    def get_contenu(self) -> str:
        return self.contenu


    def set_contenu(self, contenu: str):
        self.contenu = contenu


    # Transforme ce qui est en mémoire en un vrai fichier sur l'ordi
    def sauvegarder(self):
        """
        Sauvegarde l'e-mail dans un fichier texte.
        Le nom du fichier est basé sur l'adresse du destinataire.
        """
        # Créer un nom de fichier valide à partir de l'adresse e-mail
        nom_fichier = self.destinataire.replace('@', '_').replace('.', '_') + ".txt"
       
        try:
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                f.write(f"From: <{self.expediteur}>\n")
                f.write(f"To: <{self.destinataire}>\n")
                f.write("\n")  # Ligne vide pour séparer les en-têtes du corps
                f.write(self.contenu)
            print(f"E-mail sauvegardé dans le fichier : {nom_fichier}")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde de l'e-mail : {e}")

