from datetime import datetime, timedelta
import re
import sqlite3
import pytz

ct = pytz.timezone('US/Central')

# conn = sqlite3.connect('database.db')
# c = conn.cursor()
# c.execute("DELETE FROM events WHERE evnetStart > datetime('now');")
# conn.commit()
# conn.close()

def checkEvents() -> list:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events WHERE evnetStart < datetime('now');")
    messagesList = []
    for row in c.fetchall():
        messagesList.append((row[2], f'{row[1]}, your event *{row[3]}* has begun!'))
    c.execute("DELETE FROM events WHERE evnetStart < datetime('now');")
    conn.commit()
    conn.close()
    return messagesList

def getEvents(thisuserid:str) -> str:
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM events WHERE userid = \'{thisuserid}\' ORDER BY evnetStart ASC')
    message = ''
    now = datetime.now()
    for row in c.fetchall():
        startdate = datetime.strptime(row[4][:19], '%Y-%m-%d %H:%M:%S')
        timediff = startdate - now - timedelta(hours = 5)
        printval = startdate.replace(tzinfo=None) - timedelta(hours = 5)
        message += f'Event *{row[3]}* starts at *{printval}*   ({str(timediff)} from now).\n'
    if message == '':
        message = "Your do not have any events scheduled."
    return message

def sayHiFromScheudler(payload: dict) -> str:
    #print(payload)
    matches = re.findall(r'"([^"]*)"', payload['text'])
    if len(matches) != 3:
        return "Error: Improper /schedule format"
    try:
        myEvent = Event(payload['user_name'], payload['user_id'], matches[0], matches[1], matches[2])

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'INSERT INTO events (username, userid, eventName, evnetStart, eventEnd) VALUES ("{myEvent.username}", "{myEvent.userid}", "{myEvent.eventName}", "{myEvent.eventStart.astimezone(pytz.utc)}", "{myEvent.eventEnd.astimezone(pytz.utc)}")')
        conn.commit()
    except Exception as e:
        return "Error: {0}".format(str(e))

    return myEvent.printEvent()

class Event:
    def __init__(self, username: str, userid: str, eventName: str, eventStartStr: str, eventEndStr: str):
        self.formatString = "%Y-%m-%d %H:%M"
        self.username = username
        self.userid = userid
        self.eventName = eventName
        self.eventStart = datetime.strptime(eventStartStr, self.formatString)
        self.eventEnd = datetime.strptime(eventEndStr, self.formatString)
        if self.eventStart > self.eventEnd:
            raise Exception('Error: eventEnd is before eventStart')
            
        
    def printEvent(self):
       return f'''{self.username}, your event *{self.eventName}* starts at *{self.eventStart.astimezone(ct).strftime(self.formatString)}* and ends at *{self.eventEnd.astimezone(ct).strftime(self.formatString)}*.'''
