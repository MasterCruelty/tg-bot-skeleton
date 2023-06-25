import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *
from pyrogram import Client
from utils.get_config import *
import peewee


#Inizio della connessione con il db
db.connect()


#############################################################################    
#### FUNCTIONS LINKED TO MANAGEMENT OF SAVED GROUPS WITH AUTHORIZED COMMANDS
#############################################################################    

"""
    Return the list of authorized groups to certain commands
"""
@Client.on_message()
def list_group(client,message):
    result = "Saved groups:\n\n"
    query = Group.select()
    for group in query:
        result += str(group.id_group) + ";" + group.title + ";" + group.command + "\n"
    return sendMessage(client,message,result)


"""
    Setting the group as the only one authorized to execute a certain command
"""
@Client.on_message()
def set_group(client,message,query):
    #Split on whitespace because the input is like: /setgroup <group id> <command>
    splitted = query.split(" ")
    json_group = client.get_chat(splitted[0])
    group_id = json_group.id
    title = json_group.title
    command = splitted[1]
    
    #Insert in db
    group = Group(id_group = group_id,title = title,command = command)
    group.save()
    #Verify if insert is done correctly
    query = Group.select().where(Group.id_group == group_id)
    for item in query:
        result = "Group " + str(item.id_group) + " registered with command " + command
    return sendMessage(client,message,result)

"""
    Delete the selected group from the authorized groups to certain commands
"""
@Client.on_message()
def del_group(client,message,query):
    Group.delete().where(Group.id_group == query).execute()
    result = "Group " + str(query) + " deleted from saved groups."
    return sendMessage(client,message,result)

"""
    Update the group name on db
"""
@Client.on_message()
def update_group(client,message,query):
    json_group = client.get_chat(query)
    (Group
     .update({Group.title: json_group.title})
     .where(Group.id_group == json_group.id)).execute()
    result = "Group " + str(json_group.id ) + " updated with success!"
    return sendMessage(client,message,result)

"""
    Check if the group is authorized to execute a certain command
"""
def check_group_command(match,message):
    query = (Group
            .select()
            .where((Group.id_group == get_chat(message)) &
                   (Group.command == match))).execute()

    #check is there's at least one record
    i = 0
    for _ in query:
        i = i + 1
    if i == 0:
        return True
    else:
        return False


##############################################################    
#### FUNCTIONS LINKED TO MANAGEMENT OF USERS
##############################################################    
"""
This function do a select from User table and return all user ids in a int list
"""

def list_id_users():
    result = []
    query = User.select()
    query += Admin.select()
    for user in query:
        result.append(user.id_user)
    return result

"""
This function do a select from the user table and return the data of all registered user in a certain group.
Otherwise all user data if used in a private chat.
"""
@Client.on_message()
def list_user(client,message):
    result = "Saved users:\n\n"
    query = User.select()
    config = get_config_file("config.json")
    id_super_admin = config["id_super_admin"].split(";")
    if(int(get_chat(message)) != int(id_super_admin[0])):
        for user in query:
            try:
                client.get_chat_member(get_chat(message),user.id_user)
                result += str(user.id_user) + ";" + user.name + ";" + user.username + ";Admin: " + str(user.admin) + "\n"
            except:
                continue
    else:
        for user in query:
            result += str(user.id_user) + ";" + user.name + ";" + user.username + ";Admin: " + str(user.admin) + "\n"
    return sendMessage(client,message,result)

"""
This function is similar to list_user but return only the number of registered user
"""

def all_user(client,message):
    count = 0
    query = User.select()
    for user in query:
        count += 1
    result = "Saved users: " + str(count)
    return sendMessage(client,message,result)

"""
This function allow to register a new user in user table
"""
@Client.on_message()
def set_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    user = User(id_user = userid, name = nome_utente, username = username_utente)
    try:
        user.save()
    except:
        return sendMessage(client,message,"User already registered")
    query = User.select().where(User.id_user == userid)
    for user in query:
        result = "User " + str(user.id_user) + " saved!"
    return sendMessage(client,message,result) 

"""
    Update of db data of specific user
"""
@Client.on_message()
def update_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    (User
     .update(name = nome_utente,username = username_utente)
     .where(User.id_user == userid)).execute()
    result = "Data updated for user " + str(userid)
    return sendMessage(client,message,result)

"""
This function delete a user from the user table
"""
@Client.on_message()
def del_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.delete().where(User.id_user == userid).execute()
    result = "User " + str(userid) + " deleted."
    return sendMessage(client,message,result)

"""
This function check if a certain Telegram user is registered in User table
"""

def isUser(id_utente):
    if isSuper(id_utente) or isAdmin(id_utente):
        return True
    else:
        check = User.select().where(User.id_user == id_utente)
        for user in check:
            return True
        return False

"""
This function allow to register a new admin in User table
"""
@Client.on_message()
def set_admin(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    nome_utente = json_user.first_name
    username_utente = "@" + str(json_user.username)
    admin = User(id_user = userid, name = nome_utente, username = username_utente, admin = True)
    try:
        admin.save()
    except:
        admin = User.update({User.admin: True}).where(User.id_user == userid).execute()
        return sendMessage(client,message,"Rights added to user " + str(userid))
    query = User.select().where(User.id_user == userid)
    for admin in query:
        result = "Admin " + str(admin.id_user) + " saved!"
    return sendMessage(client,message,result)

"""
This function delete an admin from the User table
"""
@Client.on_message()
def del_admin(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.update({User.admin: False}).where(User.id_user == userid).execute()
    result = "Admin " + str(userid) + " revoked."
    return sendMessage(client,message,result) 

"""
This function check if a certain Telegram user is an admin or not
"""

def isAdmin(id_utente):
    if isSuper(id_utente):
        return True
    else:
        check = User.select().where((User.id_user == id_utente) & 
        (User.admin == True))
        for admin in check:
            return True
        return False

"""
this function check id a Telegram user is the super admin
"""

def isSuper(id_utente):
    check = User.select().where((User.id_user == id_utente) &
            ((User.superadmin == True) & 
            (User.admin == True)))
    for superadmin in check:
        return True
    return False

#chiusura della connessione con il db
db.close()
