import sqlite3
from .LoginInfoManagerInterface import LoginInfoManagerInterface


class LoginInfoChanger(LoginInfoManagerInterface):
    """
    Class to split the user's input message into usable data, change the data into the database table, and respond with an appropirate text.
    Extends LoginInfoManagerInterface, so also has capabilities to check if desired data to be set already has an entry. 
    """

    def __init__(self, userID:str, message:str):
        self.connection = sqlite3.connect('billbot.db')
        self.cursor = self.connection.cursor()
        self.userID = userID
        split_message = message.split(', ')
        self.accessCode = split_message[3]
        self.entryType = split_message[0]
        self.accountName = split_message[1]
        self.newInput = split_message[2]
        self.tableName = ''.join(['user',userID])
    

    def changeInfo(self):
        """
        Updates table entry based on data from the user's input message.
        Commits to the database connection.
        """
        self.cursor.execute("UPDATE "+self.tableName+" SET "+self.entryType+"='"+self.newInput+"' WHERE accountName='"+self.accountName+"' ")
        self.connection.commit()
    

    def responseText(self, success:bool):
        if success:
            return(' '.join([self.entryType, "successfully changed for", self.accountName]))
        else: 
            return("Data does not exist. If you wish to set your data, use the /pw-mgr-set command.")

    
    
    
