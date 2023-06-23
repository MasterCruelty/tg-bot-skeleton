from pyrogram import Client 
from utils.controller import *
from utils.dbfunctions import *
from utils.get_config import *
from utils.sysfunctions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
#bot_token only if this app is a bot, otherwise it's not needed
bot_token = config["bot_token"]
session = config["session_name"]
comandi = config["commands"][0]
comandi_admin = config["commands"][1]
comandi_super = config["commands"][2]
app = Client(session, api_id, api_hash,bot_token)
print("MIT license\nContribute @ https://www.github.com/MasterCruelty/tg-bot-skeleton\n\ntg-bot is running...")
@app.on_message()
def print_updates(client,message):
    #Get main field of incoming message
    chat = get_chat(message)
    id_messaggio = get_id_msg(message)
    utente = get_id_user(message)
    nome_chat = get_chat_name(message)
    nome_utente = get_first_name(message)
    username = get_username(message) 
    messaggio = get_text_message(message)

    
    #get the json of the message
    if "/getmessage" in str(message) and (isAdmin(utente) or isSuper(utente)):
        return get_message("",client,message)

    #super admin commands fetching
    cmd_super = comandi_super.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_super and isSuper(utente):
    #log of the super admin command recognized
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client)
        query = parser(messaggio)
        fetch_super_command(match[0],query,client,message)
        return

    #admin commands
    cmd_admin = comandi_admin.split(";")
    match = messaggio.split(" ")
    if match[0] in cmd_admin and isAdmin(utente):
    #log of the admin command recognized
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client)
        query = parser(messaggio)
        try:
            fetch_admin_command(match[0],query,client,message)
        except Exception as e:
            messaggio = messaggio + "\n\n" + str(e)
            visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client)
        return

    #user commands
    lista_comandi = comandi.split(";")
    match = messaggio.split(" ")
    if match[0] in lista_comandi and isUser(utente):
    #log of the user command recognized
        visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client)
        query = parser(messaggio)
        try:
            fetch_command(match[0],query,client,message)
        except Exception as e:
            messaggio = messaggio + "\n\n" + str(e)
            visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client)
        return
    elif match[0] in lista_comandi or messaggio == "/start":
        app.send_message(chat,"You're not registered on this bot.")

app.run()
