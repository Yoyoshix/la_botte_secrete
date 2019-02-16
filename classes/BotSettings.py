class BotSettings:
    def __init__(self, prefix):
        self.prefix = prefix
        self.state_rr = 0
        self.state_rr_true = 0
        self.rr_msg_left = 10
        self.rr_time_left = 1
        self.debug = 0
        self.update()

    def update(self, return_msg=None):
        pass

        #print(self.ping_text)
