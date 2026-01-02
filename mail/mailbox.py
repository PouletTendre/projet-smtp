import os


class Mailbox:
    
    MAILBOX_DIR = "mailboxes"
    
    def __init__(self):
        if not os.path.exists(self.MAILBOX_DIR):
            os.makedirs(self.MAILBOX_DIR)
    
    def get_mailbox_path(self, recipient):
        filename = recipient.replace("<", "").replace(">", "")
        return os.path.join(self.MAILBOX_DIR, filename + ".txt")
    
    def save_message(self, sender, recipient, data):
        path = self.get_mailbox_path(recipient)
        with open(path, "a", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("From: " + sender + "\n")
            f.write("To: " + recipient + "\n")
            f.write("\n")
            f.write(data)
            f.write("\n")
