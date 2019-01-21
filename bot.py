import discord
import json
import os
import random
import requests

from classes.MessageContent import MessageContent
from classes.ReturnMessage import ReturnMessage
from classes.CommandList import CommandList
from classes.BotSettings import BotSettings
from classes.ServerInfo import ServerInfo
from classes.Luis_data import Luis_data

#incomplet
CMD_LIST = ["ping", "pong", "help", "test", "update", "option", "rr", "we"]

bot = discord.Client() #Initialize bot
exe = CommandList() #Initialize cmd available
bot_sett = BotSettings() #Initialize bot settings
serv = ServerInfo(bot, discord) #initialize server info
luis = Luis_data()

@bot.event
async def on_message(message):
    if (message.author == bot.user):
        #print(message.content)
        if (message.content[0] == "#"):
            serv.add_message_to_delete(message)
            print("SHOULD BE ADDED :", serv.message_to_delete_content)
        return

    if len(message.content) == 0:
        return

    return_msg = ReturnMessage()
    msg = MessageContent(message)

    if msg.author in luis.target_user:
        luis.process_msg(msg, return_msg)

    if msg.prefix == "?":
        if msg.cmd == "ping":
            exe.ping(msg, return_msg)
        if msg.cmd == "pong":
            exe.pong(return_msg)
        if msg.cmd == "help":
            exe.help(return_msg)
        if msg.cmd == "test":
            exe.test(discord, msg, bot, bot_sett, serv, return_msg)
        if msg.cmd == "update":
            exe.update(bot, bot_sett, serv, return_msg)
        if msg.cmd == "option":
            exe.option(msg.msg_split, return_msg)
        if msg.cmd == "mute" or msg.cmd == "unmute":
            await exe.mute_or_unmute(discord, msg, bot, serv, return_msg)
        if msg.cmd == "rr" or msg.cmd == "trr":
            exe.option(msg, return_msg)
        if msg.cmd == "luis":
            luis.add_user(msg, return_msg)
        if msg.cmd == "servstate":
            serv.get_state(return_msg)
        if msg.cmd == "plot":
            exe.plot(msg, return_msg)
        if msg.cmd == "say":
            exe.say(msg, return_msg)
        if msg.cmd == "debug_parse":
            exe.debug_parse(msg, return_msg)

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

    bot_msg = return_msg.make_answer()
    if (bot_msg != ""):
        await bot.send_message(message.channel, bot_msg)

@bot.event
async def on_ready():
    serv.update(bot) #because we need to be connected to update infos
    print("logged in as", bot.user.name, bot.user.id)
    await bot.change_presence(game=discord.Game(name="Tourner Laurent en Bourique", type=0))

with open("auth.json") as f:
    jsnf = json.load(f)
    #print(jsnf['token'])
bot.run(jsnf['token'])

#@todo creer la cmd !joke
#@todo faire la cmd !luis ou si !luis "blablabla" alors reponse de luis direct
#@todo faire la cmd !luis ou si juste !luis alors entrer en mode luis
#@todo faire un truc de mathplotlib, save le graphic, importer le graphic sur discord
#@todo faire la gestion des roles auto
