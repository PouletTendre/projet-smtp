import socket


class SMTPClient:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connected = True
        response = self.receive()
        return response
    
    def send_command(self, command):
        if not self.connected:
            return None
        message = command + "\r\n"
        self.socket.send(message.encode("utf-8"))
        response = self.receive()
        return response
    
    def receive(self):
        data = self.socket.recv(1024)
        return data.decode("utf-8").strip()
    
    def send_mail(self, sender, recipient, subject, body):
        self.send_command("HELO localhost")
        
        response = self.send_command("MAIL FROM:<" + sender + ">")
        if not response.startswith("250"):
            return False
        
        response = self.send_command("RCPT TO:<" + recipient + ">")
        if not response.startswith("250"):
            return False
        
        response = self.send_command("DATA")
        if not response.startswith("354"):
            return False
        
        message = "Subject: " + subject + "\r\n"
        message += "\r\n"
        message += body + "\r\n"
        message += "."
        
        response = self.send_command(message)
        if not response.startswith("250"):
            return False
        
        return True
    
    def quit(self):
        if self.connected:
            self.send_command("QUIT")
            self.socket.close()
            self.connected = False
    
    def close(self):
        if self.socket:
            self.socket.close()
            self.connected = False
