

class MessageContent:
    def __init__(self, message, prefix, cmd_list):
        self.message = message.content
        self.author = message.author
        self.server = message.server
        self.channel = message.channel

        self.msg_trim = self.message.strip()
        self.msg_split = self.msg_trim.split(" ")
        while "" in self.msg_split:
            self.msg_split.remove("")

        self.cmd = ""
        if len(self.msg_split[0]) > 1 and self.msg_split[0][0] == prefix:
            self.cmd = self.msg_split[0][1:]

        self.member_mentions = message.mentions
        self.role_mentions = message.role_mentions
        self.channel_mentions = message.channel_mentions

        self.parse_msg = []
        self.parse_type = ""
        self.parse(self.msg_split, prefix, cmd_list)

    def parse_command(self, cmd, cmd_list):
        if cmd in cmd_list:
            self.parse_type += "x"
            self.parse_msg.append(cmd[1:])
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

    def is_mention_inside(self, index, list):
        for i in list:
            print("checking", index, i.id)
            if index == i.id:
                return True
        return False

    def parse_mention(self, mention):
        print("mention is", mention, type(mention))
        if self.is_mention_inside(mention[2:-1], self.member_mentions) == True:
            self.parse_type += "m"
        elif self.is_mention_inside(mention[3:-1], self.role_mentions) == True:
            self.parse_type += "r"
        elif self.is_mention_inside(mention[2:-1], self.channel_mentions) == True:
            self.parse_type += "c"
        else:
            self.parse_type += "w"
            print("LOG LOG LOG")
            with open("log.txt", "w") as f:
                f.write(mention)
        self.parse_msg.append(mention)

    def parse(self, message, prefix, cmd_list):
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

        #@todo #make the parser works for mentions

        self.parse_type = ""
        self.parse_msg = []
        for i in message:
            if i[0].isdigit():
                self.parse_number(i, "w")
            elif len(i) == 1:
                self.parse_type += "w"
                self.parse_msg.append(i)
            elif i[0] == prefix:
                self.parse_command(i, cmd_list)
            elif i[0] == "-":
                self.parse_number(i, "o", 1)
            elif i[0] == "<" and len(i) > 3:
                self.parse_mention(i)
            else:
                self.parse_type += "w"
                self.parse_msg.append(i[(i[0] == "\\"):])

    def indexes(self, ranges):
        length = len(self.parse_type)
        index_array = []

        if ranges == None:
            index_array = [i for i in range(length)]
        else:
            for i in ranges.split(","):
                if ":" not in i:
                    index_array.append(int(i))
                else:
                    limits = i.split(":")
                    for j in range(int(limits[0]),int(limits[1])):
                        index_array.append(j)
        return index_array

    def finder(self, match="w", ranges=None, positive=True, reverse=False):
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
        length = len(self.parse_type)
        index_array = self.indexes(ranges)

        target = 0
        for idx in range(length*reverse-reverse, length*(-reverse+1)-reverse, (-reverse)*2+1):
            if (self.parse_type[idx] in match) == positive:
                if target in index_array:
                    res.append(self.parse_msg[idx])
                target += 1
        return res

    def checker(self, match="xw", ranges=None, in_a_row=True, reverse=False):
        """ return True if parameters does match the parse_type
        match is the content of the parse_type elements you want to search
        in_a_row on True means that match must be a substring of parse_type.
            - Using False will check if elements in match does appear in parse_type with the order
            - Using None will just check if elements are in parse_type whatever the order is
        limits is just when to start, when to end
            - Putting negatives values here will start from the end
        reverse on True will reverse the order of the checker

        by default it returns True if there is a command and a word """

        res = []
        length = len(self.parse_type)
        index_array = self.indexes(ranges)
        substring = ""

        for idx in range(length*reverse-reverse, length*(-reverse+1)-reverse, (-reverse)*2+1):
            if idx in index_array:
                substring += self.parse_type[idx]

        if in_a_row == True:
            return (match in substring)
        if in_a_row == False:
            target = 0
            for i in substring:
                target += (match[target] == i)
            return (target == maxi)
        if in_a_row == None:
            for i in self.parse_type:
                if i in match:
                    match = match.replace(i, '', 1)
            return (match == "")
        return None
