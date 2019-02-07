

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
        self.parse_msg = []
        self.parse_type = ""
        self.parse(self.message, prefix)

    def parse_command(self, cmd):
        if cmd in CMD_LIST:
            self.parse_type += "x"
        else:
            self.parse_type += "w"
        self.parse_msg.append(cmd)
    
    def parse_number(self, value, parse_type, offset=0):
        try:
            res = int(value)
            parse_type = "i"
        except ValueError as e:
            try:
                res = float(value)
                parse_type = "f"
            except ValueError as e:
                res = value[offset:]
        self.parse_type += parse_type
        self.parse_msg.append(res)
    
    def parse_mention(self, mention):
        self.parse_type += "m"
        self.parse_msg.append(mention)
    
    def parse(self, message, prefix):
        """ return nothing but store data in self.parse_msg and self.parse_type
        This function is used to parse the given message to help getting specific parts of it
        
        'element' is a single value from message.split(" ")
        then for each elements we give a type that corresponds to its "function" in the message
        type list : cmd "x", word "w", option "o", int "i", float "f", member "m", role = "r", "channel" = "c"
        
        exemple : !ping -d 9 -moi "lol" -10 @yoyoshi @aaaaa -1a !pong !omg
        result : [ping,x] [d,o] [9,i] [moi,o] ["lol",w] [-10,i] [yoyoshi,m] [@aaaaa,w] [1a,o] [pong,x] [!omg,w]
        result is [parse_msg, parse_type]
        x,i,f,m,r,c are only attributed if the value is correct. w is used by default
        
        prefix just match the current prefix used on the server """
        
        @todo #make the parser works for mentions
        
        self.parse_type = ""
        self.parse_msg = []
        for i in message:
            if i[0] in "0123456789":
                self.parse_number(i, "w")
            elif len(i) == 1:
                self.parse_type += "w"
                self.parse_msg.append(i)
            elif i[0] == prefix:
                self.parse_command(i[1:])
            elif i[0] == "-":
                self.parse_number(i, "o", 1)
            elif i[0] == "<":
                self.parse_mention(i)
            else:
                self.parse_type += "w"
                self.parse_msg.append(i[(i[0] == "\\"):])
   
    def finder(self, target=None, match="wif", positive=True, reverse=False):
        """ return elements in the message with given parameters
        match is the type of elements you want to get (check the parse_type variable to see possibilities)
        target will create the range of elements to capture
            -None will match everything
            -it follows the same syntax as an array indexer like [0:4]
            -use ',' to add another target in the list
            -exemple : 0:2,4 will match 0,1 and 4
        positive match elements when they have the same value as positive
        reverse on True will start the research from the end 
        
        by default the finder return all words """
        
        res = []
        maxi = len(self.parse_type)
        base = [i for i in range(0, maxi)]
        index_array = []
        
        if target == None:
            index_array = base
        else:
            for i in target.split(","):
                if ":" not in i:
                    index_array.append(int(i))
                else:
                    limits = i.split(":")
                    for j in base[int(limits[0]):int(limits[1])]:
                        index_array.append(j)
        target = 0
        for idx in base[::(-reverse)*2+1]:
            if (self.parse_type[idx] in match) == positive:
                if target in index_array:
                    res.append(self.parse_msg[idx])
                target += 1
        return res

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
    """