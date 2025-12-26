"""
Module des fonctions du serveur SMTP.
Contient le gestionnaire de client qui traite les commandes SMTP.
"""

import socket
import sys
import os

# Ajouter le répertoire parent au path pour importer le module mail
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from mail.mail import Email


class GestionnaireClient:
    """
    Worker/Handler : Gère la discussion avec un client spécifique.
    Traite les commandes SMTP pour une connexion client.
    """

    def __init__(self, client_socket: socket.socket):
        """
        Constructeur pour le gestionnaire de client.
        
        :param client_socket: Le socket du client connecté.
        """
        self.client_socket = client_socket
        self.email = Email()
        self.reader = None
        self.writer = None

    def run(self):
        """
        Point d'entrée du thread pour gérer un client.
        Gère la conversation SMTP avec le client.
        """
        try:
            self.reader = self.client_socket.makefile('r')
            self.writer = self.client_socket.makefile('w')

            # Envoyer le message de bienvenue
            self.envoyer_reponse("220 Simple SMTP Server prêt à recevoir !")

            while True:
                ligne = self.reader.readline()
                if not ligne:
                    break  # Le client s'est déconnecté
                
                ligne = ligne.strip()
                print(f"Reçu du client : {ligne}")
                
                # Traiter les commandes SMTP
                if ligne.upper().startswith("MAIL FROM:"):
                    self.traiter_mail_from(ligne)
                elif ligne.upper().startswith("RCPT TO:"):
                    self.traiter_rcpt_to(ligne)
                elif ligne.upper() == "DATA":
                    self.traiter_data()
                elif ligne.upper() == "QUIT":
                    self.envoyer_reponse("221 Bye")
                    break
                else:
                    # Commande non reconnue ou non implémentée
                    self.envoyer_reponse("502 Command not implemented")

        except (ConnectionResetError, BrokenPipeError):
            print("Le client a déconnecté brutalement.")
        finally:
            self.fermer_connexion()

    def envoyer_reponse(self, reponse: str):
        """
        Envoie une réponse au client.
        
        :param reponse: La réponse à envoyer (code + message)
        """
        self.writer.write(reponse + "\r\n")
        self.writer.flush()

    def traiter_mail_from(self, ligne: str):
        """
        Traite la commande MAIL FROM.
        Extrait l'adresse de l'expéditeur.
        
        :param ligne: La ligne contenant la commande MAIL FROM
        """
        try:
            expediteur = ligne.split('<')[1].split('>')[0]
            self.email.set_expediteur(expediteur)
            self.envoyer_reponse("250 OK")
        except IndexError:
            self.envoyer_reponse("501 Syntax error in parameters")

    def traiter_rcpt_to(self, ligne: str):
        """
        Traite la commande RCPT TO.
        Extrait l'adresse du destinataire.
        
        :param ligne: La ligne contenant la commande RCPT TO
        """
        try:
            destinataire = ligne.split('<')[1].split('>')[0]
            self.email.set_destinataire(destinataire)
            self.envoyer_reponse("250 OK")
        except IndexError:
            self.envoyer_reponse("501 Syntax error in parameters")

    def traiter_data(self):
        """
        Traite la commande DATA.
        Reçoit le contenu du mail jusqu'à la ligne contenant uniquement un point.
        """
        self.envoyer_reponse("354 Start mail input, end with <CRLF>.<CRLF>")
        lignes_contenu = []
        
        while True:
            ligne = self.reader.readline()
            if not ligne:
                break
            # Arrêt quand on reçoit une ligne contenant uniquement un point
            if ligne.strip() == ".":
                break
            lignes_contenu.append(ligne)
        
        self.email.set_contenu("".join(lignes_contenu))
        self.email.sauvegarder()
        self.envoyer_reponse("250 Message accepted and saved")

    def fermer_connexion(self):
        """
        Ferme proprement la connexion avec le client.
        """
        try:
            print(f"Connexion avec {self.client_socket.getpeername()} fermée.")
        except:
            print("Connexion fermée.")
        
        if self.reader:
            self.reader.close()
        if self.writer:
            self.writer.close()
        if self.client_socket:
            self.client_socket.close()
