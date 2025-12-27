# 1. On définit la classe de base dont tout le monde hérite
class EtapeSMTP:
    def __init__(self, socket_partagee):
        self.sock = socket_partagee

    def envoyer_commande(self, commande):
        # On ajoute \r\n car le protocole SMTP l'exige à chaque fin de ligne
        self.sock.send(f"{commande}\r\n".encode())

    def lire_reponse(self):
        reponse = self.sock.recv(1024).decode()
        print(f"Serveur : {reponse.strip()}")
        return reponse

# 2. Tes classes spécialisées utilisent les outils de EtapeSMTP
class EtapeEmetteur(EtapeSMTP):
    def executer(self, email_expediteur):
        self.envoyer_commande(f"MAIL FROM:<{email_expediteur}>")
        reponse = self.lire_reponse()
        if not reponse.startswith("250"):
            print("Erreur lors de l'envoi de MAIL FROM")
            return False
        return True
class EtapeRecepteur(EtapeSMTP):
    def executer(self, email_destinataire):
        self.envoyer_commande(f"RCPT TO:<{email_destinataire}>")
        reponse = self.lire_reponse()
        if not reponse.startswith("250"):
            print("Erreur lors de l'envoi de RCPT TO")
            return False
        return True

class EtapeContenu(EtapeSMTP):
    def executer(self):
        self.envoyer_commande("DATA")
        reponse = self.lire_reponse()
        if not reponse.startswith("354"):
            print("Erreur lors de l'envoi de DATA")
            return False
        return True

class EtapeEnvoi(EtapeSMTP):
    def executer(self):
        self.envoyer_commande("QUIT")
        reponse = self.lire_reponse()   
        self.sock.close()
        if not reponse.startswith("221"):
            print("Erreur lors de l'envoi de QUIT")
            return False
        else:
            print("Email envoyé avec succès ! TERMINUS JE VAIS ME SUICIDER POUR LE BIEN DU PC !")
        return True