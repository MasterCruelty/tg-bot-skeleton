from peewee import *
import sys
sys.path.append(sys.path[0] + "/..")
from utils.get_config import get_config_file

config = get_config_file("config.json")
id_super_admin = config["id_super_admin"].split(";")
path_db = config["path_db"]

global db
db = SqliteDatabase(path_db)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id_user = IntegerField(unique = True)
    name = CharField()
    username = CharField()
    admin = BooleanField(default=False)
    superadmin = BooleanField(default=False)


"""
    Group table to authorize a command only in certain group chats.
    Fields:
    id gruppo
    nome gruppo
    nome comando
"""
class Group(BaseModel):
    id_group = IntegerField(unique = True)
    title = CharField()
    command = CharField()

db.connect()
db.create_tables([User,Group])

#Initialize the superadmin from the configuration file
overlord = User(id_user = id_super_admin[0], name = id_super_admin[1], username = id_super_admin[2], admin = True, superadmin = True)
try:
    overlord.save()
except:
    db.close()
db.close()
