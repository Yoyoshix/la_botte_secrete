import discord
import os
import random

from classes.MessageContent import MessageContent
from classes.ReturnMessage import ReturnMessage
from classes.PingDatabase import PingDatabase
from classes.CommandList import CommandList
from classes.BotSettings import BotSettings
from classes.ServerInfo import ServerInfo

client = discord.Client() #Initialize client
exe = CommandList() #Initialize cmd available
bot = BotSettings("!") #Initialize bot settings and his parameters
serv = ServerInfo(client, discord) #Initialize Server info/data
pingdtb = PingDatabase() #Load and manage data for the !ping cmd

@client.event
async def on_message(message):
    if (message.author == client.user):
        #print(message.content)
        if (message.content[0] == "#"):
            serv.add_message_to_delete(message)
            print("SHOULD BE ADDED :", serv.message_to_delete_content)
        return

    if len(message.content) == 0:
        return

    if message.content[0] == bot.prefix:
        return_msg = ReturnMessage()
        msg = MessageContent(message, bot.prefix, exe.cmd_list)

        if msg.cmd == "ping":
            exe.ping(pingdtb, msg, return_msg)
        if msg.cmd == "pong":
            exe.pong(return_msg)
        if msg.cmd == "help":
            exe.help(return_msg)
        if msg.cmd == "test":
            exe.test(discord, msg, client, bot, serv, return_msg)
        if msg.cmd == "update":
            exe.update(bot, bot, serv, return_msg)
        if msg.cmd == "option":
            exe.option(msg.msg_split, return_msg)
        if msg.cmd == "mute" or msg.cmd == "unmute":
            await exe.mute_or_unmute(discord, msg, client, serv, return_msg)
        if msg.cmd == "rr" or msg.cmd == "trr":
            exe.option(msg, return_msg)
        if msg.cmd == "servstate":
            serv.get_state(return_msg)
        if msg.cmd == "plot":
            exe.plot(msg, return_msg)
        if msg.cmd == "say":
            exe.say(msg, return_msg)
        if msg.cmd == "debug_parse":
            exe.debug_parse(msg, return_msg)

        bot_msg = return_msg.make_answer()
        if (bot_msg != ""):
            if return_msg.channel == None:
                return_msg.channel = msg.channel
            await client.send_message(return_msg.channel, bot_msg)
    else:
        pass

    #if (cmd == "test"):
    #    return_msg = test.test(msg.author)
    #if (cmd == "del"):
    #    return_msg = await delete.delete(bot, message, msg_split)
    #if (cmd == "respect @katia to @machin"):
    #    await delete.delete(msg_split)
    #    return_msg = "Katia un peu de respect pour AdrienF stp"
    #if (cmd == "grp"):
    #    return_msg = group.group(bot, msg_split)
        #return_msg = count
        #return_msg = group.group(bot, message, msg_split)

@client.event
async def on_ready():
    serv.update(client) #because we need to be connected to update infos
    print("logged in as", client.user.name, client.user.id)
    await client.change_presence(game=discord.Game(name="Tourner Laurent en Bourique", type=0))

client.run(os.environ["TOKEN"])

#@todo creer la cmd !joke
#@todo faire un truc de mathplotlib, save le graphic, importer le graphic sur discord
#@todo faire la gestion des roles auto
