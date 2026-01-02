import os
from mail.message import Message


class Mailbox:
    
    MAILBOX_DIR = "mailboxes"
    
    def __init__(self):
        if not os.path.exists(self.MAILBOX_DIR):
            os.makedirs(self.MAILBOX_DIR)
    
    def get_mailbox_path(self, recipient):
        username = recipient.split("@")[0]
        username = username.replace("<", "").replace(">", "")
        return os.path.join(self.MAILBOX_DIR, username + ".txt")
    
    def save_message(self, message):
        path = self.get_mailbox_path(message.get_recipient())
        with open(path, "a", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write(message.to_string())
            f.write("\n")
    
    def get_messages(self, recipient):
        path = self.get_mailbox_path(recipient)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
