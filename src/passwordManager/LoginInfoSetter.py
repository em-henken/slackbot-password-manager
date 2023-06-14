import sqlite3
from .LoginInfoManagerInterface import LoginInfoManagerInterface


class LoginInfoSetter(LoginInfoManagerInterface):
    """
    Class to split the user's input message into usable data, set the data into the database table, and respond with an appropirate text.
    Extends LoginInfoManagerInterface, so also has capabilities to check if desired data to be set already has an entry. 
    """

    def __init__(self, userID:str, message:str):
        self.connection = sqlite3.connect('billbot.db')
        self.cursor = self.connection.cursor()
        self.userID = userID
        split_message = message.split(', ')
        self.accessCode = split_message[3]
        self.entryType = (split_message[0].split(' '))[0]
        self.accountName = split_message[1]
        self.newInput = split_message[2]
        self.tableName = ''.join(['user',userID])


    def setInfo(self):
        """
        If user's table does not exist, create a new table.
        Insert values into the table based on data from the user's input message.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS "+self.tableName+"(accountName TEXT PRIMARY KEY, username TEXT, password TEXT)")
        try:
            self.cursor.execute("INSERT INTO "+self.tableName+" (accountName, "+self.entryType+") VALUES (?, ?)", (self.accountName, self.newInput ))
        except sqlite3.IntegrityError:
            self.cursor.execute("UPDATE "+self.tableName+" SET "+self.entryType+" = ? WHERE accountName = ?", (self.newInput, self.accountName))
        self.connection.commit()


    def responseText(self, success:bool):
        if success:
            return(' '.join([self.entryType, "successfully set for", self.accountName]))
        else: 
            return("Data already exists. If you wish to change your data, use /pw-mgr-change command")
