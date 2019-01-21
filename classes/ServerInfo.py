class ServerInfo:
    def __init__(self, bot, discord):
        self.server = discord.Server
        self.server_name = self.server.name
        self.roles = self.server.roles
        self.member_list = []
        self.message_to_delete_ref = []
        self.message_to_delete_content = []

    def update(self, bot, return_msg=None):
        self.member_list = []
        for i in bot.get_all_members():
            self.member_list.append(i)
        if return_msg != None:
            return_msg.main = "Informations updated"

    def get_member_by_role(self, role, return_msg, get_return=False):
        user_list = []
        for i in self.member_list:
            print(str(i))
            for j in i.roles:
                #print(str(j))
                if (str(j) == str(role)):
                    user_list.append(i)
                    break
        if len(user_list) == 0:
            return_msg.priority = "No user with \"" + role + "\" on this server"
        elif get_return == True:
            return_msg.priority = str(len(user_list)) + " users with \"" + role + "\" role found on this server"
        #print(user_list)
        return user_list

    def add_message_to_delete(self, message):
        self.message_to_delete_ref.append(message)
        self.message_to_delete_content.append(message.content)

    def get_message_to_delete(self, research="", position=-1):
        print(self.message_to_delete_content)
        for pos, i in enumerate(self.message_to_delete_content):
            if research == i or pos == position:
                tmp = self.message_to_delete_ref[position]
                del self.message_to_delete_ref[position]
                del self.message_to_delete_content[position]
                return tmp
        return None

    def get_state(self, return_msg):
        if len(self.message_to_delete_ref) == 0:
            return_msg.main += "msg delete is empty" + "\n"
            return
        return_msg.main = "msg delete : \n"
        for i in self.message_to_delete_content:
            return_msg.main += i + "\n"
