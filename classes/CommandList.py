import numpy as np

class CommandList:
    def __init__(self):
        self.cmd_list = dir(self)[27:] #yay, it works

    def help(self, return_msg):
        return_msg.main = "```Here is all commands with desc and current state"
        return_msg.main += "\nping [-a|-d|-l]\nDesc : Dislay a random msg\nOptions : -a to add a line. -d to delete a line. -l to get the current list\nState : Not working\n"
        return_msg.main += "\npong\nDesc : lol\n"
        return_msg.main += "\nsay\nDesc : If you want the bot say something\nState : Some issues with whole msg\n"
        return_msg.main += "\nrr\nDesc : To start the russian roulette\nState : Coming\n"
        return_msg.main += "\nrrr\nDesc : To start the real russian roulette\nState : Coming\n"
        return_msg.main += "```"

    def ping(self, pingdtb, msg, return_msg):
        def ping_add(pingdtb, msg, return_msg):
            if msg.checker("xo", "0,1") == False:
                print("checker false")
                return
            if len(msg.finder("s", start="x", keep_prefix=True, positive=False)) == None:
                return_msg.error = "Cannot create empty message for !ping\n" + \
                    "@here and @everyone are ignored"
                return_msg.channel = msg.author
            else:
                content = " ".join(msg.msg_split[2:])
                while "\n" in content:
                    print("check")
                    content = content.replace("\n", "\\n")
                pingdtb.pingdtb.append(content)
                pingdtb.save_ping_text()
                return_msg.main = "New message added. There is currently " + str(len(pingdtb.pingdtb)) + " different texts"

        def ping_delete(pingdtb, msg, return_msg):
            if msg.checker("xoi", "0,1,2") == False:
                return
            return_msg.warning = "Command not ready yet. Need to add emote detection"
            return
            id = msg.finder("i", 1)[0]
            if id < 1 or id > len(pingdtb.pingdtb):
                return_msg.error = "id is out of range"
                return_msg.channel = msg.author
            else:
                pass

        def ping_list(pingdtb, msg, return_msg):
            if msg.checker("xo", "0,1") == False:
                return
            return_msg.main = "```md\n"
            for idx, i in enumerate(pingdtb.pingdtb):
                while "\\n" in i:
                    i = i.replace("\\n", "\n")
                return_msg.main += str(idx+1) + ". " + i
            return_msg.main += "```"

        #main of ping
        if msg.checker("o", 1) == False:
            ping_text = pingdtb.pingdtb[np.random.randint(0,len(pingdtb.pingdtb))]
            while "\\n" in ping_text:
                print("check")
                ping_text = ping_text.replace("\\n", "\n")
            return_msg.main = ping_text
        else:
            option = msg.finder("o", 1)[0]
            if option == "a" or option == "add":
                ping_add(pingdtb, msg, return_msg)
            elif option == "d" or option == "delete":
                ping_delete(pingdtb, msg, return_msg)
            elif option == "l" or option == "list":
                ping_list(pingdtb, msg, return_msg)
            else:
                return_msg.error = "Unknown option '" + option + "' with ping.\n" + "Use !help !ping to get some infos"
                return_msg.channel = msg.author


    def pong(self, return_msg):
        return_msg.main = "tente un !ping plutot"

    def test(self, discord, msg, bot, bot_sett, serv, return_msg):
        #print("got =",msg.msg_trim)
        #return_msg.main = ".\n" + ", ".join(msg.parse_msg)
        #return_msg.main += "\n" + ", ".join(msg.type_list)
        res = msg.find_parse(msg.parse_msg[-1])
        if res == None:
            return_msg.error = "not find"
        else:
            return_msg.main = res

    def update(self, bot, bot_sett, serv, return_msg):
        bot_sett.update(return_msg)
        serv.update(bot, return_msg)
        return_msg.warning = "Update completed"
        return_msg.info = "~ Thanks for taking care of me"

    def option(self, msg_split, return_msg):
        pass

    async def mute_or_unmute(self, discord, msg, bot, serv, return_msg):
        if str(msg.author) != "lcetinsoy#0774" and str(msg.author) != "Yoyoshi#7181":
            return_msg.error = "Only the chosen one master of everything \"Laurent the Great\" can use !" + msg.cmd
            print(str(msg.author))
            return
        #print(len(serv.apprenant_list), serv.apprenant_list)

        user_list = serv.get_member_by_role("Apprenant", return_msg, False)
        if (len(user_list) == 0):
            #return_msg.error = "No target found"
            return

        role = discord.utils.get(msg.server.roles, name="MUTED")
        await bot.send_message(msg.channel, "# Processing")
        if msg.cmd == "mute":
            for i in user_list:
                #print(i)
                await bot.add_roles(i, role)
            return_msg.main = "Every Apprenant is now MUTED"
            return_msg.info = "~ Mind to use !unmute later :p"
        else:
            for i in user_list:
                #print(i)
                await bot.remove_roles(i, role)
            return_msg.main = "Every Apprenant is now UNMUTED"
            return_msg.info = "You can know talk about your life again"
        #print(serv.message_to_delete[0].content)
        message = serv.get_message_to_delete("# Processing")
        if message != None:
            await bot.delete_message(message)

    def plot(self, msg, return_msg):
        pass

    def say(self, msg, return_msg):
        print("k")
        return_msg.main = msg.parse_msg[msg.parse_type.index('w')]

    def get_type_name(self, type):
        if type == "x":
            return "command"
        if type == "w":
            return "word"
        if type == "o":
            return "option"
        if type == "i":
            return "int"
        if type == "f":
            return "float"
        if type == "m":
            return "member"
        if type == "r":
            return "role"
        if type == "c":
            return "channel"
        if type == "s":
            return "special"

    def debug_parse(self, msg, return_msg):
        return_msg.main = "msg is : `" + msg.message + "`\nParse gives (type, content) :\n"
        for i, j in zip(msg.parse_type, msg.parse_msg):
            if type(j) == type(" "):
                return_msg.main += self.get_type_name(i) + ", " + j + "\n"
            elif type(j) == type(0):
                return_msg.main += self.get_type_name(i) + ", " + str(j) + "\n"
            elif type(j) == type(.0):
                return_msg.main += self.get_type_name(i) + ", " + str(j) + "\n"
            else:
                try:
                    print("Special parse :", j, "\nType :", type(j))
                    return_msg.main += self.get_type_name(i) + ", " + j + "\n"
                except ValueError as e:
                    print("ERROR PARSING :", e)
