import utils_config
from pyrogram import Client

"""
Load configuration file
"""
def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)

"""
Function that send a text message 
"""
@Client.on_message()
def sendMessage(client,message,result):
    client.send_message(get_chat(message),result,disable_web_page_preview=True,reply_to_message_id=get_id_msg(message))

"""
function that send photos
"""
@Client.on_message()
def sendPhoto(client,message,result,caption):
    client.send_photo(get_chat(message),result,caption=caption,reply_to_message_id=get_id_msg(message))

"""
function that send videos
"""
@Client.on_message()
def sendVideo(client,message,result,caption):
    client.send_video(get_chat(message),result,caption=caption,file_name='video.mp4',reply_to_message_id=get_id_msg(message))

"""
function that send audio
"""
@Client.on_message()
def sendAudio(client,message,result,caption):
    client.send_audio(get_chat(message),result,caption=caption,file_name='audio.mp3',reply_to_message_id=get_id_msg(message))

"""
function that send gif
"""
@Client.on_message()
def sendGIF(client,message,result,caption):
    client.send_animation(get_chat(message),result,caption=caption,reply_to_message_id=get_id_msg(message))

"""
return the user id
"""
def get_id_user(message):
    try:
        return message.from_user.id
    except:
        return "user id not available"
"""
return the chat id
"""
def get_chat(message):
    try:
        return message.chat.id
    except AttributeError:
        print("Can't get the chat id")

"""
return the chat title
"""
def get_chat_name(message):
    try:
        return message.chat.title
    except AttributeError:
        print("can't get the chat name")

"""
return the user first name
"""
def get_first_name(message):
    try:
        return message.from_user.first_name
    except:
        return "User first name not available"
"""
return the username 
"""
def get_username(message):
    try:
        return "@" + message.from_user.username
    except:
        return "Username not existing"

"""
return the text message
"""
def get_text_message(message):
    if message.text is None:
        return "Media File"
    else:
        return message.text
"""
return the message id
"""
def get_id_msg(message):
    return message.id
