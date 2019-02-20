class PingPending:
    def __init__(self, author, target_msg=None, new_message=None):
        self.author = author
        self.target_msg = target_msg
        self.new_message = new_message
        self.pending = True

class PingDatabase:
    def __init__(self):
        self.FILE_PATH = "ping.txt"
        self.pingdtb = self.load_ping_text()
        self.waiting = False

    def load_ping_text(self):
        res = []
        while self.waiting == True:
            pass
        self.waiting = True
        with open(self.FILE_PATH, "r") as file:
            for i in file:
                offset = i.index("#") + 2
                res.append(i[offset:])
        self.waiting = False
        print("PING loaded")
        return res

    def save_ping_text(self):
        while self.waiting == True:
            pass
        self.waiting = True
        with open(self.FILE_PATH, "w") as file:
            for idx, i in enumerate(self.pingdtb):
                file.write(str(idx+1) + "# " + i)
        self.waiting = False
        print("PING saved")
        pass
