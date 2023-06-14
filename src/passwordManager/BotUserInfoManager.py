import sqlite3

class BotUserInfoManager():
    """
    Class to manage the billbotUsers table. Checks if a user already is joined in the Billbot Password Manager or not.
    Sets a new bot user into billbotUsers table with an access code.
    """

    def __init__(self):
        self.connection = sqlite3.connect('billbot.db')
        self.cursor = self.connection.cursor()


    def checkUserExists(self, userIDTag:str):
        """
        Goes into billbotUsers table and selects where the userIDTag input parameter is in the userID column.
        Then it checks if the selection is None or not.
        If None, there is no found entry and return False, else True if there is a found entry.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS billbotUsers(userID TEXT PRIMARY KEY, accessCode TEXT)")
        self.connection.commit()
        result = self.cursor.execute("SELECT ? FROM billbotUsers WHERE userID=?", (userIDTag, userIDTag))
        if (result.fetchone() == None):
            return False
        else:
            return True


    def setNewBotUser(self, userID:str, accessCodeInput:str):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS billbotUsers(userID TEXT PRIMARY KEY, accessCode TEXT)")
        self.connection.commit()
        self.cursor.execute("INSERT INTO billbotUsers (userID, accessCode) VALUES (?,?)",(userID, accessCodeInput) )
        self.connection.commit()


    def getAccessCode(self, userID:str):
        result = self.cursor.execute("SELECT accessCode FROM billbotUsers WHERE userID='"+userID+"'")
        return result.fetchone()[0] #do I need to error check this?
    

    def closeConnection(self):
        self.connection.close()
