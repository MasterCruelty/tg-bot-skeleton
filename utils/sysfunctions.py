from pyrogram import Client
from pyrogram import errors
import utils.controller as uct
import utils.get_config as ugc
import random
import os
import sys


"""
Return the entire json of a Telegram message. If the json is over the message capacity, it will be saved on a text file and sended.
"""
@Client.on_message()
def get_message(query,client,message):
    chat = ugc.get_chat(message)
    uct.save_json(message)
    client.send_document(chat,document = "json_message.json",caption = "__Here the json of the message__",reply_to_message_id=message.id)

"""
Ping the bot to check if it's on
"""
def ping(query,client,message):
    return ugc.sendMessage(client,message,"pong " + query.replace("/pingrob",""))

"""
Restart the bot
"""
def restart(client,message):
    ugc.sendMessage(client,message,"__Restarting...\n\nIn ten seconds I should be on again.__")
    os.execl(sys.executable,sys.executable,*sys.argv)

"""
Documentation of user commands directly on Telegram with a command
"""
def help(query,client,message):
    help_file = ugc.get_config_file("help.json")
    if query in help_file:
        help_request = help_file[query][0:]
        help_request = str(help_request).replace("(","").replace(")","").replace('"','').replace(r'\n','\n')
        return ugc.sendMessage(client,message,help_request)
    elif (query not in help_file) and (query != "/helprob"):
        help_request = "__**Command not found**__\n\n"
        help_request += help_file["default"]
        return ugc.sendMessage(client,message,help_request)
    else:
        help_request = help_file["default"]
        return ugc.sendMessage(client,message,help_request)
