from mail.mailbox import Mailbox


class SMTPHandler:
    
    def __init__(self):
        self.mailbox = Mailbox()
        self.reset_state()
    
    def reset_state(self):
        self.sender = None
        self.recipient = None
        self.data_mode = False
        self.data_buffer = []
    
    def handle_command(self, line):
        if self.data_mode:
            return self.handle_data_content(line)
        
        line = line.strip()
        if not line:
            return None
        
        command = line.split()[0].upper()
        
        if command == "MAIL":
            return self.handle_mail(line)
        elif command == "RCPT":
            return self.handle_rcpt(line)
        elif command == "DATA":
            return self.handle_data()
        elif command == "QUIT":
            return "221 Au revoir"
        else:
            return "500 Commande non reconnue"
    
    def handle_mail(self, line):
        upper_line = line.upper()
        if "FROM:" not in upper_line:
            return "501 Syntaxe: MAIL FROM:<adresse>"
        
        start = line.find("<")
        end = line.find(">")
        if start != -1 and end != -1:
            self.sender = line[start+1:end]
        else:
            parts = line.split(":")
            self.sender = parts[1].strip()
        return "250 OK"
    
    def handle_rcpt(self, line):
        if self.sender is None:
            return "503 MAIL requis avant RCPT"
        
        upper_line = line.upper()
        if "TO:" not in upper_line:
            return "501 Syntaxe: RCPT TO:<adresse>"
        
        start = line.find("<")
        end = line.find(">")
        if start != -1 and end != -1:
            self.recipient = line[start+1:end]
        else:
            parts = line.split(":")
            self.recipient = parts[1].strip()
        return "250 OK"
    
    def handle_data(self):
        if self.sender is None:
            return "503 MAIL requis avant DATA"
        if self.recipient is None:
            return "503 RCPT requis avant DATA"
        
        self.data_mode = True
        self.data_buffer = []
        return "354 Entrez le message, terminez par un point"
    
    def handle_data_content(self, line):
        if line.strip() == ".":
            self.data_mode = False
            data = "\n".join(self.data_buffer)
            self.mailbox.save_message(self.sender, self.recipient, data)
            self.reset_state()
            return "250 Message accepte"
        else:
            self.data_buffer.append(line.rstrip("\r\n"))
            return None
    
    def is_quit(self, line):
        return line.strip().upper() == "QUIT"
