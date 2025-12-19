import socket
from email import Email


class GestionnaireClient:
   
    #Worker/Handler : Gère la discussion avec un client spécifique
    # Initialise avec le socket (le tuyau) du client déjà connecté
    def __init__(self, client_socket: socket.socket):
        """
        Constructeur pour le gestionnaire de client.
        :param client_socket: Le socket du client connecté.
        """
        self.client_socket = client_socket
        self.email = Email()
        self.reader = None
        self.writer = None
    # Le début !
    def run(self):
        #Point d'entrée du thread pour gérer un client.
        try:
            self.reader = self.client_socket.makefile('r')
            self.writer = self.client_socket.makefile('w')


            # Envoyer le message de bienvenue
            self.envoyer_reponse("220 Simple SMTP Server prét à recevoir !")


            while True: # J'attends une commande (texte) du client !
                ligne = self.reader.readline()
                if not ligne:
                    break  # bon ben le client ne veut plus discuter...
               
                ligne = ligne.strip()
                print(f"Reçu du client : {ligne}")
                # Il va lire ligne par ligne ce que l'on va envoyer et interpréter ligne par ligne ce qu'il doit faire
                if ligne.upper().startswith("MAIL FROM:") : # Dans le standard SMTP RFC 5321, la toute première chose qu'un client envoie est HELO.
                    self.traiter_mail_from(ligne)
                elif ligne.upper().startswith("RCPT TO:"):
                    self.traiter_rcpt_to(ligne)
                elif ligne.upper() == "DATA":
                    self.traiter_data()
                elif ligne.upper() == "QUIT":
                    self.envoyer_reponse("221 Bye")
                    break
                else:
                    # Commande non reconnue ou non implémentée dans cette version
                    self.envoyer_reponse("502 Command not implemented")
        # Erreur soudaine
        except (ConnectionResetError, BrokenPipeError):
            print("Le client a déconnecté brutalement.")
        finally:
            self.fermer_connexion()
    # Prend le texte que nous souhaitons envoyer et gére les sauts de lignes
    def envoyer_reponse(self, reponse: str):
        # Envoie une réponse au client.
        self.writer.write(reponse + "\r\n")
        self.writer.flush()
    # Découpe la ligne pour extraire uniquement l'@ mail située <entre> . Elle l'a stock dans l'objet email
    def traiter_mail_from(self, ligne: str):
        """Traite la commande MAIL FROM."""
        try:
            expediteur = ligne.split('<')[1].split('>')[0]
            self.email.set_expediteur(expediteur)
            self.envoyer_reponse("250 OK")
        except IndexError:
            self.envoyer_reponse("501 Syntax error in parameters")
    # Elle extrait l'@ de destination.
    def traiter_rcpt_to(self, ligne: str):
        """Traite la commande RCPT TO."""
        try:
            destinataire = ligne.split('<')[1].split('>')[0]
            self.email.set_destinataire(destinataire)
            self.envoyer_reponse("250 OK")
        except IndexError:
            self.envoyer_reponse("501 Syntax error in parameters")
    # Elle prévient le client qu'il peut commencer à écrire (envoyer le corps du mail)
    def traiter_data(self):
        self.envoyer_reponse("354 Start mail input, end with <CRLF>.<CRLF>")
        lignes_contenu = []
        while True:
            ligne = self.reader.readline()
            if not ligne:
                break
            # s'arrete quand elle voit une simple ligne avec un .
            if ligne.strip() == ".":
                break
            lignes_contenu.append(ligne)
       
        self.email.set_contenu("".join(lignes_contenu))
        self.email.sauvegarder()
        self.envoyer_reponse("250 Message accepted and saved")


    # Ferme tout !
    def fermer_connexion(self):
        print(f"Connexion avec {self.client_socket.getpeername()} fermée.")
        if self.reader:
            self.reader.close()
        if self.writer:
            self.writer.close()
        if self.client_socket:
            self.client_socket.close()