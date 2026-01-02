from datetime import datetime


class Message:
    
    def __init__(self, sender, recipient, data):
        self.sender = sender
        self.recipient = recipient
        self.data = data
        self.date = datetime.now()
    
    def get_sender(self):
        return self.sender
    
    def get_recipient(self):
        return self.recipient
    
    def get_data(self):
        return self.data
    
    def get_date(self):
        return self.date
    
    def to_string(self):
        result = "From: " + self.sender + "\n"
        result += "To: " + self.recipient + "\n"
        result += "Date: " + self.date.strftime("%Y-%m-%d %H:%M:%S") + "\n"
        result += "\n"
        result += self.data
        return result
