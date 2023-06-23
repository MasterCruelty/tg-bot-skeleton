import sys
sys.path.append(sys.path[0] + "/..")
from utils.dbtables import *
from pyrogram import Client
from utils.get_config import *
import peewee


#Inizio della connessione con il db
db.connect()


#############################################################################    
#### FUNZIONI LEGATE ALLA GESTIONE DEI GRUPPI SALVATI CON COMANDI AUTORIZZATI
#############################################################################    

"""
    Restituisce la lista dei gruppi autorizzati a certi comandi
"""
@Client.on_message()
def list_group(client,message):
    result = "Gruppi salvati:\n\n"
    query = Group.select()
    for group in query:
        result += str(group.id_group) + ";" + group.title + ";" + group.command + "\n"
    return sendMessage(client,message,result)


"""
    setto il gruppo come unico autorizzato a un particolare comando
"""
@Client.on_message()
def set_group(client,message,query):
    #splitto sullo spazio poichè l'input è del tipo /setgroup <id gruppo> <comando>
    splitted = query.split(" ")
    json_group = client.get_chat(splitted[0])
    group_id = json_group.id
    title = json_group.title
    command = splitted[1]
    
    #inserisco in db
    group = Group(id_group = group_id,title = title,command = command)
    group.save()
    #verifico sia inserito correttamente
    query = Group.select().where(Group.id_group == group_id)
    for item in query:
        result = "Gruppo " + str(item.id_group) + " registrato con comando " + command
    return sendMessage(client,message,result)

"""
    Cancella il gruppo selezionato dai gruppi autorizzati a determinati comandi
"""
@Client.on_message()
def del_group(client,message,query):
    Group.delete().where(Group.id_group == query).execute()
    result = "Gruppo " + str(query) + " eliminato dai gruppi salvati."
    return sendMessage(client,message,result)

"""
    Aggiorna il nome di un gruppo sul db
"""
@Client.on_message()
def update_group(client,message,query):
    json_group = client.get_chat(query)
    (Group
     .update({Group.title: json_group.title})
     .where(Group.id_group == json_group.id)).execute()
    result = "Gruppo " + str(json_group.id ) + " aggiornato con successo!"
    return sendMessage(client,message,result)

"""
    controllo se il gruppo è autorizzato a eseguire un determinato comando
"""
def check_group_command(match,message):
    query = (Group
            .select()
            .where((Group.id_group == get_chat(message)) &
                   (Group.command == match))).execute()

    #controllo se vi è almeno un record
    i = 0
    for _ in query:
        i = i + 1
    if i == 0:
        return True
    else:
        return False


##############################################################    
#### FUNZIONI LEGATE ALLA GESTIONE DEGLI UTENTI SALVATI SUL DB
##############################################################    
"""
questa funzione fa una select dalla tabella User e restituisce gli id di tutti gli utenti registratii dentro una lista di int
"""

def list_id_users():
    result = []
    query = User.select()
    query += Admin.select()
    for user in query:
        result.append(user.id_user)
    return result

"""
questa funzione fa una select dalla tabella User e restituisce i dati di tutti gli utenti in un dato gruppo.
Oppure tutti gli utenti se dato il comando in chat privata
"""
@Client.on_message()
def list_user(client,message):
    result = "Lista utenti salvati:\n\n"
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
questa funzione è simile a list_user ma restituisce solo il numero degli utenti registrati nella tabella User
"""

def all_user(client,message):
    count = 0
    query = User.select()
    for user in query:
        count += 1
    result = "Totale utenti registrati: " + str(count)
    return sendMessage(client,message,result)

"""
questa funzione permette di registrare un nuovo utente nella tabella User
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
        return sendMessage(client,message,"Utente già registrato")
    query = User.select().where(User.id_user == userid)
    for user in query:
        result = "Utente " + str(user.id_user) + " salvato!"
    return sendMessage(client,message,result) 

"""
    update dei dati sul db di un utente specifico
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
    result = "Dati aggiornati per utente " + str(userid)
    return sendMessage(client,message,result)

"""
Questa funzione elimina un utente dalla tabella User
"""
@Client.on_message()
def del_user(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.delete().where(User.id_user == userid).execute()
    result = "Utente " + str(userid) + " eliminato."
    return sendMessage(client,message,result)

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella User
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
questa funzione permette di registrare un nuovo admin nella tabella Admin
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
        return sendMessage(client,message,"Permessi admin aggiunti a " + str(userid))
    query = User.select().where(User.id_user == userid)
    for admin in query:
        result = "Admin " + str(admin.id_user) + " salvato!"
    return sendMessage(client,message,result)

"""
Questa funzione elimina un admin  dalla tabella Admin
"""
@Client.on_message()
def del_admin(client,message,query):
    json_user = client.get_users(query)
    userid = json_user.id
    query = User.update({User.admin: False}).where(User.id_user == userid).execute()
    result = "Admin " + str(userid) + " revocato."
    return sendMessage(client,message,result) 

"""
Questa funzione controlla se un certo utente Telegram è registrato nella tabella Admin
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
Questa funzione controlla se un certo utente Telegram è SuperAdmin
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
