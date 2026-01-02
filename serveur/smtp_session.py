from serveur.smtp_handler import SMTPHandler


class SMTPSession:
    
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        self.handler = SMTPHandler()
        self.running = True
        self.buffer = ""
    
    def start(self):
        print("Connexion de " + str(self.client_address))
        self.send_response("220 Serveur SMTP pret")
        
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                
                self.buffer += data.decode("utf-8")
                
                while "\r\n" in self.buffer or "\n" in self.buffer:
                    if "\r\n" in self.buffer:
                        line, self.buffer = self.buffer.split("\r\n", 1)
                    else:
                        line, self.buffer = self.buffer.split("\n", 1)
                    
                    response = self.handler.handle_command(line)
                    
                    if response is not None:
                        self.send_response(response)
                    
                    if self.handler.is_quit(line):
                        self.running = False
                        break
                    
            except Exception as e:
                print("Erreur session: " + str(e))
                break
        
        self.close()
    
    def send_response(self, response):
        message = response + "\r\n"
        self.client_socket.send(message.encode("utf-8"))
    
    def close(self):
        print("Fermeture connexion " + str(self.client_address))
        self.client_socket.close()
