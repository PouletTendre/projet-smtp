"""
Module des fonctions du client SMTP.
Contient les classes pour envoyer des emails via SMTP.
"""

import socket


class ClientSMTP:
    """
    Classe pour envoyer des emails via SMTP.
    Gère la connexion et l'envoi des commandes au serveur.
    """

    def __init__(self, host: str, port: int):
        """
        Initialise le client SMTP.
        
        :param host: Adresse du serveur SMTP
        :param port: Port du serveur SMTP
        """
        self.host = host
        self.port = port
        self.socket = None
        self.reader = None
        self.writer = None

    def connecter(self):
        """
        Établit la connexion avec le serveur SMTP.
        
        :return: True si la connexion réussit, False sinon
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            self.reader = self.socket.makefile('r')
            self.writer = self.socket.makefile('w')
            
            # Lire le message de bienvenue du serveur
            reponse = self.lire_reponse()
            print(f"Serveur: {reponse}")
            
            return reponse.startswith("220")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
            return False

    def lire_reponse(self) -> str:
        """
        Lit la réponse du serveur.
        
        :return: La réponse du serveur
        """
        reponse = self.reader.readline().strip()
        return reponse

    def envoyer_commande(self, commande: str) -> str:
        """
        Envoie une commande au serveur et retourne la réponse.
        
        :param commande: La commande à envoyer
        :return: La réponse du serveur
        """
        self.writer.write(commande + "\r\n")
        self.writer.flush()
        print(f"Client: {commande}")
        
        reponse = self.lire_reponse()
        print(f"Serveur: {reponse}")
        return reponse

    def envoyer_mail(self, expediteur: str, destinataire: str, contenu: str) -> bool:
        """
        Envoie un email complet.
        
        :param expediteur: Adresse de l'expéditeur
        :param destinataire: Adresse du destinataire
        :param contenu: Contenu du message
        :return: True si l'envoi réussit, False sinon
        """
        try:
            # Commande MAIL FROM
            reponse = self.envoyer_commande(f"MAIL FROM:<{expediteur}>")
            if not reponse.startswith("250"):
                print("❌ Erreur lors de l'envoi de MAIL FROM")
                return False

            # Commande RCPT TO
            reponse = self.envoyer_commande(f"RCPT TO:<{destinataire}>")
            if not reponse.startswith("250"):
                print("❌ Erreur lors de l'envoi de RCPT TO")
                return False

            # Commande DATA
            reponse = self.envoyer_commande("DATA")
            if not reponse.startswith("354"):
                print("❌ Erreur lors de l'envoi de DATA")
                return False

            # Envoi du contenu
            self.writer.write(contenu)
            if not contenu.endswith("\n"):
                self.writer.write("\n")
            self.writer.write(".\r\n")
            self.writer.flush()
            print("Client: [Contenu du message]")
            print("Client: .")
            
            reponse = self.lire_reponse()
            print(f"Serveur: {reponse}")
            
            if reponse.startswith("250"):
                print("✅ Message envoyé avec succès !")
                return True
            else:
                print("❌ Erreur lors de l'envoi du message")
                return False

        except Exception as e:
            print(f"❌ Erreur lors de l'envoi : {e}")
            return False

    def deconnecter(self):
        """
        Ferme proprement la connexion avec le serveur.
        """
        try:
            if self.writer and self.socket:
                self.envoyer_commande("QUIT")
        except:
            pass
        finally:
            if self.reader:
                self.reader.close()
            if self.writer:
                self.writer.close()
            if self.socket:
                self.socket.close()
            print("🔌 Déconnecté du serveur.")
