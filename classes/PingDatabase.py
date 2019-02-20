class PingDatabase:
    def __init__(self):
        self.FILE_PATH = "ping.txt"
        self.waiting = False
        self.pingdtb = self.load_ping_text()

    def load_ping_text(self):
        res = []
        while self.waiting == True:
            print("waiting")
        self.waiting = True
        with open(self.FILE_PATH, "r") as file:
            for i in file:
                offset = i.index("#") + 2
                res.append(i[offset:-1])
        self.waiting = False
        print("PING loaded")
        return res

    def save_ping_text(self):
        while self.waiting == True:
            print("waiting")
        self.waiting = True
        with open(self.FILE_PATH, "w") as file:
            for idx, i in enumerate(self.pingdtb):
                file.write(str(idx+1) + "# " + i + "\n")
        self.waiting = False
        print("PING saved")
        pass
