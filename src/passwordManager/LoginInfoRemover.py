import sqlite3
from .LoginInfoManagerInterface import LoginInfoManagerInterface


class LoginInfoRemover(LoginInfoManagerInterface):
    """
    Class to split the user's input message into usable data, remove the data from the database table, and respond with an appropirate text.
    Extends LoginInfoManagerInterface, so also has capabilities to check if desired data to be set already has an entry. 
    """
    
    def __init__(self, userID:str, message:str):
        """
        Initializes database connection for the object, and defines attributes from the input message.
        Create user table name.
        """
        self.connection = sqlite3.connect('billbot.db')
        self.cursor = self.connection.cursor()
        self.userID = userID
        split_message = message.split(', ')
        self.accessCode = split_message[1]
        self.accountName = split_message[0]
        self.tableName = ''.join(['user',userID])


    def removeInfo(self):
        """
        Removes the row in the user's table, based on data from the user's input message.
        Commits to the database connection.
        """
        self.cursor.execute("DELETE FROM "+self.tableName+" WHERE accountName=?", (self.accountName,))
        self.connection.commit()


    def responseText(self, success:bool):
        if success:
            return(' '.join(["All login data removed for", self.accountName, "."]))
        else: 
            return("There is no data to remove. To set data, use the /pw-mgr-set command.")
        
    
    def checkInfoExists(self):
        """
        Tries to select the row of the desired account name from the user's table.
        If a selection is found, return true. If not return false. Also return false if exception is raised.
        """
        try:
            result = self.cursor.execute("SELECT * FROM "+self.tableName+" WHERE accountName=?", (self.accountName,))
            row = result.fetchone()
            if (row is not None and row[0] is not None):
                return True
            else:
                return False
        except sqlite3.OperationalError:
            print('Database error: checkInfoExists()')
