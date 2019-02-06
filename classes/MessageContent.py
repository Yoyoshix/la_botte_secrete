

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
        self.cmd = ""
        if len(self.msg_split[0]) > 1 and self.prefix == prefix:
            self.cmd = self.msg_split[0][1:]
        self.parse_msg(prefix)

    def parse_command(self, cmd):
        if cmd in CMD_LIST:
            self.parse_type.append("x")
        else:
            self.parse_type.append("w")
        self.parse_msg.append(cmd)
    
    def parse_number(self, value, parse_type):
        try:
            res = int(value)
            parse_type = "i"
        except ValueError as e:
            try:
                res = float(value)
                parse_type = "f"
            except ValueError as e:
                res = value
        self.parse_type.append(parse_type)
        self.parse_msg.append(value)
    
    def parse_mention(self, mention):
        self.parse_type.append("m")
        self.parse_msg.append(mention)
    
    def parse_msg(self, prefix):
        #type : cmd "x", option "o", word "w", int "i", float "f", member "m", role = "r", "channel" = "c"
        #!ping -d 9 -moi "lol" -10 @yoyoshi @aaaaa -1a !pong !omg
        #[ping,x] , [d,o] , [9,i] , [moi,o] , ["lol",w] , [-10,i] , [yoyoshi, m] , [@aaaaa, w] , [1a,o] , [pong,x] , [!omg,w]
        #x,i,f,m,r,c are only attributed if the value is correct. !omg is not a valid command therefor it will be considered as w
        
        self.parse_type = []
        self.parse_msg = []
        for i in self.msg_split:
            if i[0] in ["0123456789"]:
                self.parse_number(i, "w")
            elif len(i) == 1:
                self.parse_type.append("w")
                self.parse_msg.append(i)
            elif i[0] == prefix:
                self.parse_command(i[1:])
            elif i[0] == "-":
                self.parse_number(i[1:], "o"):
            elif i[0] == "<":
                self.parse_mention(i)
            else:
                self.parse_type.append("w")
                self.parse_msg.append(i[(i[0] == "\\"):])
    """
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
    """
    
    def finder(index=1, match="w", positive=True, reversed=False):
        res = []
        index_array = []
        maxi = len(msg.parse_type)+1
        if type(index) == type(0):
            if index == 0:
                index_array = [i for i in range(1, maxi)]
            else:
                index_array = [index]
        else:
            start = index[0]
            end = (index[1] == 0) * maxi + (index[1] != 0) * index[1]
            index_array = [i for i in range(start, end)]
        
        for idx, parse_type, parse_msg in enumerate(zip(msg.parse_type[::((-reversed)*2+1)], msg.parse_msg[::((-reversed)*2+1)])):
            if (parse_type in match) == positive:
                res.append(parse_msg)
        return res
    
    def check(regex, specific=False):
        
    """
    possible regex maker : finder(index=1, match="w", positive=true, reversed=False)
    index is the answer you'll get when they respect the index. Index 0 is "all"
    match will match all the given parse_type //to complete someday
    if positive is false then it will match where regex is false
    reversed start the research from the end
    
    check maker : check(regex, specific=False)
    create a regex on the parse_type
    specific == true means "must match all the parse_type"
    """
