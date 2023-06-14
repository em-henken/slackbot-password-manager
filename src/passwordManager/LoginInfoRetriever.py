import sqlite3
from .LoginInfoManagerInterface import LoginInfoManagerInterface


class LoginInfoRetriever(LoginInfoManagerInterface):
    """
    Class to split the user's input message into usable data, retrieve the data from the database table, and respond with an appropirate text.
    Extends LoginInfoManagerInterface, so also has capabilities to check if desired data to be set already has an entry. 
    """

    def __init__(self, userID:str, message:str):
        self.connection = sqlite3.connect('billbot.db')
        self.cursor = self.connection.cursor()
        self.userID = userID
        split_message = message.split(', ')
        self.accessCode = split_message[2]
        self.entryType = split_message[0]
        self.accountName = split_message[1]
        self.tableName = ''.join(['user',userID])


    def retrieveInfo(self):
        """
        Selects data from the username/password column the row in the user's table, based on data from the user's input message.
        Returns the selection.
        """
        selection = self.cursor.execute("SELECT "+self.entryType+" FROM "+self.tableName+" WHERE accountName=?", (self.accountName,))
        row = selection.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


    def responseText(self, success:bool, output:str): #override interface's constructor, 2 vs 3 parameters.
        if success:
            return(' '.join([self.entryType, "for", self.accountName, ":", output]))
        else: 
            return("Data does not exist. If you wish to set your data, use /pw-mgr-set command.")
