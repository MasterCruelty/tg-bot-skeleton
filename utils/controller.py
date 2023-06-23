from pyrogram import Client
import utils_config
import modules.test
import utils.dbfunctions as udb
import utils.sysfunctions as usys
import utils.get_config as ugc

dictionary = {      '/test'           : modules.test.test_fetch,
                    '/help'           : usys.help}

dictionary_admin = {'/getmessage'     : usys.get_message,
                    '/ping'           : usys.ping}

dictionary_super = {'/setuser'        : udb.set_user,
                    '/deluser'        : udb.del_user,
                    '/updateuser'     : udb.update_user,
                    '/listuser'       : udb.list_user,
                    '/alluser'        : udb.all_user,
                    '/setadmin'       : udb.set_admin,
                    '/deladmin'       : udb.del_admin,
                    '/setgroup'       : udb.set_group,
                    '/listgroup'      : udb.list_group,
                    '/delgroup'       : udb.del_group,
                    '/updategroup'    : udb.update_group,
                    '/allamounts'     : udb.show_all_amounts,
                    '/setamount'      : udb.set_amount,
                    '/updatestat'     : udb.force_update_stats,
                    '/restart'        : usys.restart,
                    '/delstat'        : udb.force_delete_stats}

auth_command = ["/trivial"]

"""
   This function take as argument the user command recognized from the main and launch execution of the right linked module function.
"""
def fetch_command(match,query,client,message):
    #check on commands authorized in certain group chats.
    if udb.check_group_command(match,message) and match in auth_command:
        return ugc.sendMessage(client,message,"__Command not authorized in this chat.\nContact the admin @nickname.")
    else:
        udb.update_stats(ugc.get_id_user(message),match)
        dictionary[match](query,client,message)
"""
   The same as fetch_command, but for admin's command.
"""
def fetch_admin_command(match,query,client,message):
    #system functions
    udb.update_stats(ugc.get_id_user(message),match)
    dictionary_admin[match](query,client,message)

"""
   The same as fetch_command, but for super admin's command.
"""
def fetch_super_command(match,query,client,message):
    #db functions
    try:
        dictionary_super[match](client,message,query)
    except:
        dictionary_super[match](client,message)
"""
    This function helps to parse the query linked to the command launched by the user.
"""
def parser(message):
    temp = message.split(" ",1)
    try:
        result = temp[1]
    except:
        result = temp[0]
    return result

"""
    This function save on file the json of the message required.
"""
def save_json(message):
    nome_file = "json_message.json"
    save = open(nome_file,'w')
    save.write(str(message))
    save.close()


"""
    This function visualize the log of incoming messages.
"""
#I take the super admin data to send him the log
config = ugc.get_config_file("config.json")
id_super_admin = config["id_super_admin"].split(";")[0]

@Client.on_message()
def visualizza(chat,nome_chat,utente,nome_utente,username,messaggio,client):
    result = "id utente: " + str(utente) + "\nnome utente: " + nome_utente + "\nusername: " + username
    print("id_utente: " + str(utente) + "\nnome_utente: " + nome_utente + "\nusername: " + username)
    if str(chat):
        result += "\nchat id: " + str(chat) + "\nnome chat: " + str(nome_chat) + "\nmessaggio: " + messaggio
        print("chat_id: " + str(chat) + "\nnome_chat: " + str(nome_chat))
        print("messaggio: " + messaggio)
        print("**************************************************************************************")
    client.send_message(id_super_admin,result)
