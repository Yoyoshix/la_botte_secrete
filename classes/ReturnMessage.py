class ReturnMessage:
    def __init__(self, main="", error="", warning="", priority="", info="", got_cmd=False):
        self.main = main
        self.error = error
        self.warning = warning
        self.priority = priority
        self.info = info
        self.got_cmd = got_cmd

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
