

class MessageContent:
    def __init__(self, message, prefix):
        self.message = message.content
        self.author = message.author
        self.server = message.server
        self.channel = message.channel

        self.msg_trim = self.message.strip()
        self.msg_split = self.msg_trim.split(" ")
        while "" in self.msg_split:
            self.msg_split.remove("")
        self.prefix = self.msg_split[0][0]
        self.cmd = ""
        if len(self.msg_split[0]) > 1:
            self.cmd = self.msg_split[0][1:]
        self.parse_msg()

    def parse_msg(self):
        #type : cmd "x", option "o", mention "m", word "w", quote "q", value "v"
        #!ping "bonjour" -d -a 10 -moi "lol" 9
        #!ping -"bon jour -10 " oui c'est moi"

        print("got\n", self.msg_trim)
        self.parse_type = []
        self.parse_msg = []
        buffer = ""
        type = None
        if (self.msg_trim[0] == prefix):
            type = "x"
        i = 0
        while i < len(self.msg_trim):
            buffer = ""
            if (self.msg_trim[i] == "\\"):
                buffer += self.msg_trim[i+1]
                i += 2
                if (type == None):
                    type = "w"
            if (type == None and self.msg_trim[i] != " "):
                #print("read =", self.msg_trim[i])
                type = "w"
                if (self.msg_trim[i] == "-"):
                    type = "o"
                if (self.msg_trim[i].isdigit() == True):
                    type = "v"
                if (self.msg_trim[i] == "<"):
                    type = "m"
                if (self.msg_trim[i] == "\"" or self.msg_trim[i] == "'"):
                    save = self.msg_trim[i]
                    type = "q"
                    i += 1
            if (type == "q"):
                while i < len(self.msg_trim) and self.msg_trim[i] != save:
                    if (self.msg_trim[i] == "\\"):
                        buffer += self.msg_trim[i+1]
                        i += 2
                    else:
                        buffer += self.msg_trim[i]
                        i += 1
            elif (type == "m"):
                while i < len(self.msg_trim) and self.msg_trim[i] != ">":
                    buffer += self.msg_trim[i]
                    i += 1
                if i < len(self.msg_trim):
                    buffer += self.msg_trim[i]
            else:
                while i < len(self.msg_trim) and self.msg_trim[i] != " ":
                    buffer += self.msg_trim[i]
                    i += 1

            if type == "m":
                if len(buffer) >= 3:
                    if buffer[1] == "#" and buffer[2:-1] is in message.channel_mentions:
                        type = "c"
                    elif buffer[1:3] == "@!" and buffer[3:-1] is in message.mentions:
                        type = "m"
                    elif buffer[1:3] == "@&" and buffer[3:-1] is in message.role_mentions:
                        type = "r"
                    else:
                        type = "w"
                else:
                    type = "w"

            if (type == "o"):
                try:
                    #print("buf =", buffer)
                    test = int(buffer)
                    type = "v"
                except ValueError:
                    if (len(buffer) == 1):
                        type = "w"
                        buffer = "-"
                    else:
                        buffer = buffer[1:]
                        type = "o"
            #if (buffer != ""):
            if (type != None):
                if (type == "q"):
                    type = "w"
                self.parse_type.append(type)
                self.parse_msg.append(buffer)
                type = None
            i += 1

    def mention_is_inside(self, finder, list):
        for i in list:
            print("finder", finder, i.id)
            if finder == i.id:
                return True
        return False

    def find_parse(self, finder, order="first"): #find
        print(self.parse_type)
        if (order != "first"):
            finder = finder[::-1]
        pos = -1
        for i in finder:
            pos += 1
            while pos < len(self.parse_type):
                if i == self.parse_type[pos]:
                    print(self.parse_msg[pos])
                    break
                pos += 1
        if pos == len(self.parse_type):
            return None
        return self.parse_msg[pos]

    def find_all(self, finder): #find 
        res = []
        for index, i in enumerate(self.parse_type):
            if i in finder:
                res.append(self.parse_msg[index])
        if len(res) == 0:
            return None
        return res

    def find_is_exact(self, finder):
        if len(finder) != len(self.parse_type):
            return False
        for idx, i in enumerate(finder):
            if i != self.parse_type[idx]:
                return False
        return True
    
    #def find_all_next(self, finder):
    #    for idx, i in enumerate(self.parse_type):
    #       if i in finder:
    #           res.append(self.parse_msg[idx])
