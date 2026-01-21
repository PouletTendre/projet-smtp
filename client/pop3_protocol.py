"""Module client POP3.

Permet de recevoir des mails via le protocole POP3.
"""

import socket


class POP3Client:
    """Classe client pour recuperer des mails d'un serveur POP3."""

    def __init__(self, host, port):
        """Initialise le client avec l'adresse et le port du serveur."""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.file_handle = None

    def connect(self):
        """Etablit la connexion avec le serveur POP3."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.connected = True
        # Utilisation d'un file object pour faciliter la lecture ligne par ligne
        self.file_handle = self.socket.makefile('r', encoding='utf-8')
        return self._receive_line()

    def _send_command(self, command):
        """Envoie une commande au serveur."""
        if not self.connected:
            return
        message = command + "\r\n"
        self.socket.send(message.encode("utf-8"))

    def _receive_line(self):
        """Recoit une ligne de reponse."""
        if not self.file_handle:
            return ""
        return self.file_handle.readline().strip()

    def _receive_multiline(self):
        """Recoit une reponse sur plusieurs lignes (terminee par .)."""
        lines = []
        while True:
            line = self.file_handle.readline()
            if not line:
                break
            line = line.strip()
            if line == ".":
                break
            lines.append(line)
        return "\n".join(lines)

    def authenticate(self, username, password):
        """Authentifie l'utilisateur."""
        self._send_command(f"USER {username}")
        response = self._receive_line()
        if not response.startswith("+OK"):
            return False, response

        self._send_command(f"PASS {password}")
        response = self._receive_line()
        if not response.startswith("+OK"):
            return False, response
        
        return True, response

    def list_messages(self):
        """Recupere la liste des messages."""
        self._send_command("LIST")
        response = self._receive_line()
        if not response.startswith("+OK"):
            return None
        return self._receive_multiline()

    def retrieve_message(self, msg_id):
        """Recupere le contenu d'un message."""
        self._send_command(f"RETR {msg_id}")
        response = self._receive_line()
        if not response.startswith("+OK"):
            return None
        return self._receive_multiline()

    def quit(self):
        """Ferme la session."""
        if self.connected:
            self._send_command("QUIT")
            self.socket.close()
            self.connected = False

    def close(self):
        """Ferme la connexion brutalement."""
        if self.socket:
            self.socket.close()
            self.connected = False