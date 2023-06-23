from utils.get_config import sendMessage


def test_fetch(query,client,message):
    if "-d" in query:
        return sendMessage(client,message,"I'm the test default inside multiple test commands!")
    elif "-ad" in query:
        return sendMessage(client,message,"I'm the test advanced!")
    elif "-w" in query:
        return sendMessage(client,message,"I'm the test weak!")
    elif "-al" in query:
        return sendMessage(client,message,"I'm the test alone!")
    else:
        return sendMessage(client,message,"test not found!")
