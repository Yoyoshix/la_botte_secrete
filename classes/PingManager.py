class PingPending:
    def __init__(self, author, target_msg=None, new_message=None):
        self.author = author
        self.target_msg = target_msg
        self.new_message = new_message
        self.pending = True

class PingDatabase:
    def __init__(self):
        self.pingdtb = self.load_ping_text()

    def load_ping_text(self):
        res = []
        with open("ping.txt", "r") as file:
            for i in file:
                offset = i.index("#") + 2
                res.append(i[offset:])
        return res

    def save_ping_text(self):
        
        pass
