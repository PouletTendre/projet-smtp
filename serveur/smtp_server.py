import socket
from serveur.smtp_session import SMTPSession


class SMTPServer:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_ecoute = None
        self.running = False
    
    def start(self):
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_ecoute.bind((self.host, self.port))
        self.socket_ecoute.listen(5)
        self.running = True
        
        print("Serveur SMTP demarre sur le port " + str(self.port) + "...")
        print("En attente de connexions...")
        
        while self.running:
            try:
                client_socket, client_address = self.socket_ecoute.accept()
                session = SMTPSession(client_socket, client_address)
                session.start()
            except KeyboardInterrupt:
                print("Arret du serveur demande par l'utilisateur...")
                self.stop()
            except Exception as e:
                print("Erreur serveur: " + str(e))
    
    def stop(self):
        self.running = False
        if self.socket_ecoute:
            self.socket_ecoute.close()
        print("Serveur arrete.")
