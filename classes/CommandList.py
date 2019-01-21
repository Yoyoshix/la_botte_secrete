import numpy as np

class CommandList:
    def help(self, return_msg):
        return_msg.main = "```Here is all commands with desc and current state"
        return_msg.main += "\nping [-a|-d|-l]\nDesc : Dislay a random msg\nOptions : -a for adding a line. -d for delete a line. -l to get the current list\nState : Not working\n"
        return_msg.main += "\npong\nDesc : lol\n"
        return_msg.main += "\nsay\nDesc : If you want the bot say something\nState : Some issues with whole msg\n"
        return_msg.main += "\nrr\nDesc : To start the russian roulette\nState : Coming\n"
        return_msg.main += "\nrrr\nDesc : To start the real russian roulette\nState : Coming\n"
        return_msg.main += "```"
    
    def ping_write():
        pass

    def ping(self, msg, return_msg):
        ping_text = []
        length = 0
        with open("ping.txt", 'r') as f:
            for line in f:
                if "#" in line:
                    position = line.index("#")
                    if (position != -1):
                        ping_text.append(line[position+2:])
                        length += 1
                else:
                    ping_text[length-1] += line

        if len(msg.options) == 0:
            if len(ping_text) == 0:
                return_msg.warning = "There is no message I can use, add message with !ping -a"
                return
            return_msg.main = ping_text[np.random.random_integers(0, length-1)]
            return

        if msg.options[0] == "l":
            if length == 0:
                return_msg.warning = "There is no message I can use"
                return_msg.info = "FEED MEEEEE"
                return
            return_msg.priority = "Ping text list :"
            for index, i in enumerate(ping_text):
                return_msg.main += str(index) + "# " + i

        elif msg.options[0] == "a":
            pos = msg.msg_trim.index("-a")
            res = msg.msg_trim[pos+3:].strip().replace("\n", "\\n")
            if len(res) == 0:
                return_msg.error = "Can't add no text"
                return
            with open("ping.txt", 'a') as f:
                f.write(str(length) + "# " + res + "\n")
            return_msg.main = "Succesfully added \"" + res + "\" as #" + str(length)

        elif msg.options[0] == "d" or msg.options[0] == "r":
            if len(msg.values) == 0:
                return_msg.error = "Need a number"
                return
            value = msg.values[0]
            if value >= length or value < 0:
                return_msg.error = "No text at index " + str(value)
                return
            tmp = ping_text[value]
            del ping_text[value]
            with open("ping.txt", 'w') as f:
                for index, i in enumerate(ping_text):
                    f.write(str(index) + "# " + i)
            return_msg.main = "\"" + tmp[:-1] + "\" got deleted"

        elif msg.options[0] == "c" or msg.options[0] == "m":
            if len(msg.values) == 0:
                return_msg.error = "Need a number"
                return
            value = msg.values[0]
            if value >= length or value < 0:
                return_msg.error = "No text at index " + str(value)
                return
            tmp = ping_text[value]
            del ping_text[value]
            with open("ping.txt", 'w') as f:
                for index, i in enumerate(ping_text):
                    f.write(str(index) + "# " + i)
            return_msg.main = "\"" + tmp[:-1] + "\" got deleted"
            pos = msg.msg_trim.index("-a")
            res = msg.msg_trim[pos+3:].strip().replace("\n", "\\n")
            if len(res) == 0:
                return_msg.error = "Can't add no text"
                return
            with open("ping.txt", 'a') as f:
                f.write(str(length) + "# " + res + "\n")
            return_msg.main = "Succesfully added \"" + res + "\" as #" + str(length)

        else:
            return_msg.warning = "This option doesn't exist"

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

    def debug_parse(self, msg, return_msg):
        return_msg.main = "msg is : `" + msg.message + "`\nParse gives (type, content) :\n"
        for i, j in zip(msg.parse_type, msg.parse_msg):
            return_msg.main += i + ", " + j + "\n"
