from abc import ABC, abstractmethod
from .BotUserInfoManager import BotUserInfoManager
import sqlite3

class LoginInfoManagerInterface():
    
    @abstractmethod
    def __init__(userID, message:str):
        pass


    @abstractmethod
    def responseText(self, success:bool):
        pass

    
    def getAccessCode(self):
        return self.accessCode


    def closeConnection(self):
        self.connection.close()
        #self.cursor.close()


    def checkInfoExists(self):
        try:
            query = "SELECT {} FROM {} WHERE accountName=?".format(self.entryType, self.tableName)
            result = self.cursor.execute(query, (self.accountName,))
            row = result.fetchone()
            if (row is not None and row [0] is not None):
                return True
            else:
                return False
        except sqlite3.OperationalError:
            print('Database OperationalError: checkInfoExists()')
