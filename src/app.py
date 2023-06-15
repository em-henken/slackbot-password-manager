import os
from queue import Empty, Full
import random
import re

from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from passwordManager.LoginInfoRetriever import LoginInfoRetriever
from passwordManager.LoginInfoSetter import LoginInfoSetter
from passwordManager.LoginInfoRemover import LoginInfoRemover
from passwordManager.LoginInfoChanger import LoginInfoChanger
from passwordManager.BotUserInfoManager import BotUserInfoManager



# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


""" App Functions """

@app.message("hello")
def message_hello(message, say):
     # say() sends a message to the channel where the event was triggered
    say(f"Hello comrade <@{message['user']}>!")


@app.command("/pw-manager-get")
def appGetInfo(ack, body, respond):
    """
    The sender of the message will provide what data they want. A LoginInfoRetreiever object is instantiated,
    as well as a BotUserInfoManager object to verify the access code. The Retriever object checks the desired
    info exists. If so, it returns it to the user from the user's table. If not, it calls the alternate response text.
    """
    ack()
    userID = body['user_id']
    getter = LoginInfoRetriever(userID, body['text'])
    botUserMgr = BotUserInfoManager()
    if botUserMgr.checkUserExists(userID):
        if (getter.getAccessCode() != botUserMgr.getAccessCode(userID)):
            respond("Please try again with the correct access code.")
        else:
            if getter.checkInfoExists():
                output = getter.retrieveInfo()
                respond(getter.responseText(True, output))
            else:
                respond(getter.responseText(False, 'none'))
    else:
        respond("You are not a billbot databse user. use /pw-manager-join to join.")
    getter.closeConnection()
    botUserMgr.closeConnection()


@app.command("/pw-manager-set")
def appSetInfo(ack, body, respond):
    """
    The sender of the message will provide what data they want to set. A LoginInfoSetter object is instantiated,
    as well as a BotUserInfoManager object to verify the access code. The Setter object checks the desired
    info exists. If not, it goes into the user's table and set the data. Otherwise, it calls the alternate response text.
    """
    ack()
    userID = body['user_id']
    setter = LoginInfoSetter(userID, body['text'])
    botUserMgr = BotUserInfoManager()
    if botUserMgr.checkUserExists(userID):
        if (setter.getAccessCode() != botUserMgr.getAccessCode(userID)):
            respond("Please try again with the correct access code.")
        else:
            if setter.checkInfoExists():
                respond(setter.responseText(False))
            else:
                setter.setInfo()
                respond(setter.responseText(True))
    else:
        respond("You are not a billbot database user. use /pw-manager-join to join.")
    setter.closeConnection()
    botUserMgr.closeConnection()


@app.command("/pw-manager-change")
def appChangeInfo(ack, body, respond):
    """
    The sender of the message will provide what data they want to change. A LoginInfoChanger object is instantiated,
    as well as a BotUserInfoManager object to verify the access code. The Changer object checks the desired
    info exists. If so, it goes into the user's table and change the data. If not, it calls the alternate response text.
    """
    ack()
    userID = body['user_id']
    changer = LoginInfoChanger(userID, body['text'])
    botUserMgr = BotUserInfoManager()
    if botUserMgr.checkUserExists(userID):
        if (changer.getAccessCode() != botUserMgr.getAccessCode(userID)):
            respond("Please try again with the correct access code.")
        else:
            if changer.checkInfoExists():
                changer.changeInfo()
                respond(changer.responseText(True))
            else:
                respond(changer.responseText(False))
    else:
        respond("You are not a billbot database user. use /pw-manager-join to join.")
    changer.closeConnection()
    botUserMgr.closeConnection()


@app.command("/pw-manager-remove")
def appRemoveInfo(ack, body, respond):
    """
    The sender of the message will provide what account data they want to remove. A LoginInfoRemover object is instantiated,
    as well as a BotUserInfoManager object to verify the access code. The Remover object checks the desired
    info exists. If so, it goes into the user's table and remove the row. If not, it calls the alternate response text.
    """
    ack()
    userID = body['user_id']
    remover = LoginInfoRemover(userID, body['text'])
    botUserMgr = BotUserInfoManager()
    if botUserMgr.checkUserExists(userID):
        if (remover.getAccessCode() != botUserMgr.getAccessCode(userID)):
            respond("Please try again with the correct access code.")
        else:
            if remover.checkInfoExists():
                remover.removeInfo()
                respond(remover.responseText(True))
            else:
                respond(remover.responseText(False))
    else:
        respond("You are not a billbot database user. use /pw-manager-join to join.")
    remover.closeConnection()
    botUserMgr.closeConnection()


@app.command("/pw-manager-join" )
def appAddBillbotUser(ack, body, respond):
    """
    The sender of the message will include their personal access code. A BotUserInfoManager object will verify they are a new user.
    If so, it sets them up in the billbotUsers table. If not, it tells them they already are a user.
    """
    ack()
    accessCodeInput = body['text'].split(' ', 1)[0]
    userID = body['user_id']
    botUserMgr = BotUserInfoManager()
    if (botUserMgr.checkUserExists(userID)):
        respond("You already have a BillBot password account. Use the slash commands to set, change, remove, and retrieve data.")
    else:
        botUserMgr.setNewBotUser(userID, accessCodeInput)
        botUserMgr.closeConnection()
        respond("Welcome! You can now use Billiken Bot to store usernames and passwords. Use the slash commands to set, change, remove, and retrieve data.")


client = WebClient(token= os.environ['SLACK_BOT_TOKEN'])

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
