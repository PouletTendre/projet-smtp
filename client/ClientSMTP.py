import socket
from client_steps import *

# orchestrateur du Client
class ClientSMTP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # socket.socket = constructeur, AF (Adresse Family) INET (IPv4), je communique en IPv4. SOCK_STREAM, je me connecte en TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def starto(self):
        self.sock.connect((self.host, self.port))
        EmailExpe = input ("Saisir l'@ de l'expediteur : ")
        EmailDest = input ("Saisir l'@ de l'expediteur : ")
        payload = f"Sujet : {sujet} \r\n\r\n{contenu} \r\n. \r\n"
        # On utilise une méthode d'envoi brute (sans ajouter \r\n automatiquement à la fin)
        self.sock.send(payload.encode())
# On suit les différentes étapes ! 
        etape1 = EtapeEmetteur(self.sock)
        etape1.executer(EmailExpe)
        etape2 = EtapeRecepteur(self.sock)
        etape2.executer(EmailDest)
        etape3 = EtapeContenu(self.sock)
        etape3.executer()
        etape4 = EtapeEnvoi(self.sock)
        etape4.executer()

if __name__ == "__main__":
    client = ClientSMTP("localhost", 2525)
    client.starto()