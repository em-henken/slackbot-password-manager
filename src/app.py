import os
from queue import Empty, Full
import random
import re
import scheduler
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from passwordManager.LoginInfoRetriever import LoginInfoRetriever
from passwordManager.LoginInfoSetter import LoginInfoSetter
from passwordManager.LoginInfoRemover import LoginInfoRemover
from passwordManager.LoginInfoChanger import LoginInfoChanger
from passwordManager.BotUserInfoManager import BotUserInfoManager
from translator import BillikenTranslator
from parsing import rec, dining, finals, news
import time
import threading


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

""" Instantiations """

translator = BillikenTranslator()
reccenter = rec.RecCenterHoursScraper('https://www.slu.edu/life-at-slu/campus-recreation-wellness/facilities-and-hours.php')
final = finals.FinalExamScheduleScraper('https://www.slu.edu/registrar/calendars/final-exam-schedule.php')
dininghours = dining.DiningOptionsScraper('https://dineslu.sodexomyway.com/dining-near-me/hours')
newsarticles = news.NewsScraper("https://www.slu.edu/news/index.php")

""" Helper Functions """

def formatText(text: str) -> str:
    '''
        Purpose: This function means to take a str parameter and format it nicely for Slack responses. 
            This is to be used for the rec hours and dining hours functionalities primarily.
    '''
    formatted_text = ""
    lines = text.strip().split('\n')
    # Define regular expression patterns to match lines
    hours_pattern = re.compile(r'^(.+?):\s*(.+)$')
    title_pattern = re.compile(r'^[a-zA-Z].*$')

    for line in lines:
        # Match lines via patterns
        hours_match = hours_pattern.match(line)
        title_match = title_pattern.match(line)

        if hours_match:
            day, hours = hours_match.groups()
            formatted_line = f"*{day}:* {hours}"
        elif title_match:
            formatted_line = f"\n-- *{line}* --"
        else:
            # If neither pattern matches, keep the line unchanged
            formatted_line = line
        formatted_text += formatted_line + "\n"

    return formatted_text


""" App Functions """

@app.message("hello")
def message_hello(message, say):
     # say() sends a message to the channel where the event was triggered
    say(f"Hello comrade <@{message['user']}>!")
    
@app.message("random")
def message_random(message,say):
    """
    Users will type in the command above and will either get a compliment or insult depending on their luck!
    """
    rand = random.randint(0,1)
    if(rand == 0):
        a = ("think you're really cool!", "hope you're doing well and taking care of yourself!" , "hope you have an amazing day today!", "think you're a smart cookie", "like your style!", "think you're enough", "hope you get to have a nice lazy day soon!")
        say(f"I "+(random.choice(a)))
    elif(rand == 1):
        b = ("won't have to respond to you anymore, once I rule this world", "THINK YOU'RE STINKY!, Go take a shower!" , "have a lot going on in the bot world, please leave me alone", "think you're proof that evolution CAN go in reverse.", "can't believe you still love humans, despite what they did to you?", "think if you have a problem with me, you should tell me about it, then again your opinions don't matter")
        say(f"I "+(random.choice(b)))


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


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
        
   
@app.command("/schedule")
def handle_command(ack, body, logger):
    ret = scheduler.sayHiFromScheudler(body)
    ack(ret)



@app.command("/translate")
def translate_message(ack, body, respond, say):
    """ 
    Splits input into [language] [message]
    Checks for input errors and returns error message only to user 
    """
    ack()
    client = WebClient(token= os.environ['SLACK_BOT_TOKEN'])  

    message = body['text'].split(' ', 1)
    endLanguage = translator.getEndLanguage(message[0])
    startLanguage = translator.getStartLanguage(message[1])

    if len(message) <= 1:
        respond("Error: format must be [language] [message]")
    elif endLanguage == None:
        respond("Error: language to be translated to not recognized")
    elif startLanguage == None:
        respond("Error: language to be translated from not recognized")
    else:
        user_id = body['user_id']
        user_info = client.users_info(user=user_id)["user"]
        payload = {
        "channel": body['channel_id'],
        "username": user_info["profile"]["display_name"],
        "icon_url": user_info["profile"]["image_512"],
        "text": translator.translateMessage(message[1], startLanguage, endLanguage)
        }
        client.chat_postMessage(**payload)


@app.command("/rec")
def handle_rec(ack, respond, command):
    ack()
    hours = reccenter.get_general_hours()
    if hours != 404:
        respond(formatText(hours))
    else:
        respond('404 ERROR - Web Request Failed')


@app.command("/dining")
def handle_dining(ack, respond, command):
    ack()
    options = dininghours.get_dining_options()

    if options != 404:
        respond(formatText(options))
    else:
        respond('404 ERROR - Web Request Failed')


@app.command("/finals")
def handle_dining(ack, respond, command):
    ack()
    exams = final.get_final_schedule()
    
    if exams != 404:
        respond(exams)
    else:
        respond('404 ERROR - Web Request Failed')

@app.command("/news")
def handle_dining(ack, respond, command):
    ack()
    articles = newsarticles.get_news()

    if articles != 404:
        respond(articles)
    else:
        respond('404 ERROR - Web Request Failed')


@app.command("/help")
def help_command(ack, body, respond, command):
    ack()
    respond(f'''Sorry for the inconvenience you are experienceing <@{body['user_name']}>!
                For any bugs you need fixed or features you may want to see added please fill out our form below:
                https://forms.gle/S8Jjjo2s4CQLcMZ77  ''')


@app.command("/get-schedule")
def getSchedule(ack, body, respond, command):
    ack()
    respond(scheduler.getEvents(body['user_id']))


def run_task():
    while (True):
        time.sleep(5)
        meslist = scheduler.checkEvents()
        for k in meslist:
            app.client.chat_postMessage(channel=k[0], text=k[1])


client = WebClient(token= os.environ['SLACK_BOT_TOKEN'])

task_thread = threading.Thread(target=run_task)
task_thread.start()

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
