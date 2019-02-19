class ReturnMessage:
    def __init__(self, main="", error="", warning="", priority="", info="", got_cmd=False):
        self.error = error         #msg that will be highlighted with ``` + with some colors
        self.warning = warning     #msg that will be highlighted with `
        self.priority = priority   #msg that will be printed before main
        self.main = main           #msg that will be printed normally
        self.info = info           #msg that will be printed in italic in last
        self.target = None         #id of channel to send this message, can be private. If None, send the message to message.channel
        #self.got_cmd = got_cmd     #wtf ???

    def make_answer(self):
        answer = ""
        if (self.error != ""):
            self.error = "```Markdown\n#Error : " + self.error + "```\n"
            return self.error
        if (self.warning != ""):
            answer += "`" + self.warning + "`\n"
        if (self.priority != ""):
            answer += self.priority + "\n"
        if self.main != "" and self.main != []:
            print(type(self.main), type([]), self.main)
            if type(self.main) == type([]):
                print("inside")
                self.main = ", ".join(self.main)
                print(type(self.main), "|", self.main, "|")
            answer += self.main + "\n"
        if (self.info != ""):
            answer += "*" + self.info + "*\n"
        print(answer)
        return answer
