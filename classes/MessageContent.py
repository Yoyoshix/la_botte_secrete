""" This part of the program integrates key informations contained in message.content

The most important part here is the parser
It answers to the problematic of good syntaxic commands that can be hard to manage.
    Questions such as "did the user send a value ?", "is there the -a option ?"

So the idea is to segment each words (part of messages separated by a space)
    and giving them a code (by a unique char) about their property.
There is currently 8 differents elements
w : a word. Used by default
x : a valid command. If the command does not exist it will be considered as a 'w'
o : an option. When the user use a "-"
i : an integer. Note that "-10" is considered as an integer, not an option
f : a float.
c : a valid channel.
r : a valid role.
m : a valid member.
s : special. Currently, only @everyone and @here are registered here.
    This last category is useful to avoid capturing them with finder("w")

Once parsing is done it stores data into two variable, self.parse_type and self.parse_msg
Then, you can use the checker() function which helps you check if the current message
    follows specific rules. It will also helps you manage errors on your side
    when user enters a bad syntaxic comand
You can also use the finder() function to get specific parts of the message that you
    consider important and then process them easily

Note : On the discord.py documentation it says that mentions contained in the message
    that you can access with message.xxx_mentions are not necessary in the order in
    which they appear. This parser promises that the order will be correct.
    You can know create some commands like !hug @someone from @admin
"""

class MessageContent:
    def __init__(self, message, prefix, cmd_list):
        self.message = message.content
        self.author = message.author
        self.server = message.server
        self.channel = message.channel

        self.member_mentions = message.mentions
        self.role_mentions = message.role_mentions
        self.channel_mentions = message.channel_mentions

        self.msg_trim = self.message.strip()
        self.msg_split = self.msg_trim.split(" ")
        while "" in self.msg_split:
            self.msg_split.remove("")

        self.cmd = ""
        if len(self.msg_split[0]) > 1 and self.msg_split[0][0] == prefix:
            self.cmd = self.msg_split[0][1:]

        self.parse_msg = []
        self.parse_type = ""
        self.parse(self.msg_split, prefix, cmd_list)

    def parse_command(self, cmd, cmd_list):
        if cmd[1:] in cmd_list:
            self.parse_type += "x"
        else:
            self.parse_type += "w"
        self.parse_msg.append(cmd)

    #parse the option at the same time
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

        exemple : !ping -d 9 -moi "lol" -10 @yoyoshi @aaaaa -1a !pong !omg
        result : [ping,x] [d,o] [9,i] [moi,o] ["lol",w] [-10,i] [yoyoshi,m] [@aaaaa,w] [1a,o] [pong,x] [!omg,w]
        result is [parse_msg, parse_type]
        x,i,f,m,r,c are only attributed if the value is correct. w is used by default

        prefix just match the current prefix used on the server """

        self.parse_type = ""
        self.parse_msg = []
        for i in message:
            if i[0].isdigit():
                self.parse_number(i, "w")
            elif len(i) == 1:
                self.parse_type += "w"
                self.parse_msg.append(i)
            elif i == "@everyone" or i == "@here":
                self.parse_type += "s"
                self.parse_msg.append(i)
            elif i[0] == prefix:
                self.parse_command(i, cmd_list)
            elif i[0] == "-":
                self.parse_number(i, "o")
            elif i[0] == "<" and len(i) > 3:
                self.parse_mention(i)
            else:
                self.parse_type += "w"
                self.parse_msg.append(i[(i[0] == "\\"):])

    def indexes(self, ranges, offset=0):
        length = len(self.parse_type)
        index_array = []

        if ranges is None:
            index_array = [i for i in range(length)]
        else:
            for i in ranges.split(","):
                if ":" not in i:
                    index_array.append(int(i)-offset)
                else:
                    limits = i.split(":")
                    for j in range(int(limits[0]),int(limits[1])+offset):
                        index_array.append(j-offset)
        return index_array

    def finder(self, match="w", occurences=None, start=None, stop=None, trigger=True, positive=True, reverse=False, keep_prefix=False):
        """ return elements in the message with given parameters
        match is the type of elements you want to get (check the parse_type variable to see possibilities)
            using ! at start of match will reverse the value of positive
        occurences will create the nth indexes elements to capture
            -None will find everything
            -use ':' to make a range of capture, be careful as it is inclusive
            -use ',' to add another capture in the list
            -exemple : 1:3,5 will match the first, second, third and fifth occurence
        start and stop will respectively start and stop the finder on the first value they are intended to be trigger
            you can give them a number as an index OR gives them a range of parse_type
            stop is exclusive. It means that if start=stop nothing will be returned
        trigger on False will check stop only once start has been triggered. True will not
            You might get an unexpected result if start=2, stop=1, Trigger=False
                Like this, stop will not be evaluated and the finder will check elements[2:]
            Very useful when you want to start on a specific index and end on a specific parse_type after the index
        positive will match elements when they have the same value as positive
        reverse on True will reverse the order of the research
        keep_prefix on True will keep the "-" for options as well as the cmd prefix when the content will be returned

        by default the finder return all words """

        res = []
        length = len(self.parse_type)
        if occurences != None:
            occurences = str(occurences)
        index_array = self.indexes(occurences, 1)
        is_capturing = (start == None)
        target = 0
        if match == None:
            match = "xwoifmrcs"
        if len(match) > 0 and match[0] == "!":
            positive = (positive == False)

        for idx in range(length*reverse-reverse, length*(-reverse+1)-reverse, (-reverse)*2+1): #xd lol
            if is_capturing == False:
                if type(start) == type(0):
                    is_capturing = (idx == start)
                else:
                    is_capturing = (self.parse_type[idx] in start)
            if stop != None:
                if trigger == True or is_capturing == True:
                    if type(stop) == type(0) and (idx == stop):
                        break
                    if type(stop) == " " and (self.parse_type[idx] in stop):
                        break
            if is_capturing == True:
                if (self.parse_type[idx] in match) == positive:
                    if target in index_array:
                        res.append(self.parse_msg[idx][(keep_prefix == False and self.parse_type[idx] in "ox"):])
                    target += 1
        if len(res) == 0:
            return None
        return res

    def checker(self, match="xw", ranges="0,1", in_a_row=True, reverse=False):
        """ return True if parameters does match the parse_type
        match is the amount of each parse_type elements you want to search.
            You can write www to check 3 words in a row
        ranges follow the same syntax as occurences except it targets indexes
            it means that ranges="0:2,3" will only check index 0,1 and 3 in the parse_type array
        in_a_row on True means that match must be a substring of parse_type.
            - Using False will check if elements in match does appear in parse_type with the order
            - Using None will just check if elements are in parse_type whatever the order is
        reverse is the same as in finder() above

        by default it returns True if there is a command followed by a word at start """

        res = []
        length = len(self.parse_type)
        if ranges != None:
            ranges = str(ranges)
        index_array = self.indexes(ranges)
        substring = ""

        for idx in range(length*reverse-reverse, length*(-reverse+1)-reverse, (-reverse)*2+1): #xd lol
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

""" Exemples :
You want to check if the command does have a number and get it.
You also want the command to respect this syntax : xwi
use checker like this : checker("xwi", "0:2")
if it returns True you can then call the finder
like this : finder("i", 1)
we know the message does have a number, finder will return the only integer
you can also use directly MessageContent.parse_msg[2] because you are sure
the number is at index 2

"""
