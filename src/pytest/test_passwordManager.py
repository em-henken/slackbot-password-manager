import pytest
import sqlite3
import sys
sys.path.append('../../')
from src.passwordManager.LoginInfoSetter import LoginInfoSetter
from src.passwordManager.LoginInfoRetriever import LoginInfoRetriever
from src.passwordManager.LoginInfoRemover import LoginInfoRemover
from src.passwordManager.LoginInfoChanger import LoginInfoChanger
from src.passwordManager.BotUserInfoManager import BotUserInfoManager


""" 
SETTER TESTS 
"""
def test_setter_initMessageSplit():
    input = "TESTentryType, TESTaccountName, TESTinput, TESTcode"
    setter = LoginInfoSetter('PYTESTID', input)
    assert setter.entryType == 'TESTentryType'
    assert setter.accountName == 'TESTaccountName'
    assert setter.newInput == 'TESTinput'
    assert setter.accessCode == 'TESTcode'
    assert setter.tableName == 'userPYTESTID'

def test_setter_responseText():
    input = "username, TESTaccountName, TESTinput, PYTESTCODE"
    setter = LoginInfoSetter('PYTESTID', input)
    trueText = "username successfully set for TESTaccountName"
    assert setter.responseText(True) == trueText
    falseText = "Data already exists. If you wish to change your data, use /pw-mgr-change command"
    assert setter.responseText(False) == falseText

def test_setInfo():
    input = "username, TESTSETTERaccountName, TESTSETTERinput, PYTESTCODE"
    setter = LoginInfoSetter('PYTESTID', input)
    test_conn = sqlite3.connect('billbot.db')
    test_cur = test_conn.cursor()
    setter.setInfo()
    query = "SELECT username FROM userPYTESTID WHERE accountName=?"
    result = test_cur.execute(query, (setter.accountName,))
    row = result.fetchone()
    test_conn.close()
    assert row != None
    assert row == ('TESTSETTERinput',)

def test_getter_getAccessCode():
    input = "username, PYTESTaccountName, TESTinput, PYTESTCODE"
    setter = LoginInfoSetter('PYTESTID', input)
    assert setter.getAccessCode() == 'PYTESTCODE'

""" 
RETRIEVER TESTS 
"""
def test_getter_initMessageSplit():
    input = "TESTentryType, TESTaccountName, TESTcode"
    getter = LoginInfoRetriever('PYTESTID', input)
    assert getter.entryType == 'TESTentryType'
    assert getter.accountName == 'TESTaccountName'
    assert getter.accessCode == 'TESTcode'
    assert getter.tableName == 'userPYTESTID'

def test_getter_responseText():
    input = "TESTentryType, PYTESTaccountName, TESTcode"
    getter = LoginInfoRetriever('PYTESTID', input)
    res = getter.responseText(True, 'TESTOUTPUT')
    assert res ==  "TESTentryType for PYTESTaccountName : TESTOUTPUT"
    res = getter.responseText(False, 'none')
    assert res == "Data does not exist. If you wish to set your data, use /pw-mgr-set command."

def test_getter_getAccessCode():
    input = "username, PYTESTaccountName, PYTESTCODE"
    getter = LoginInfoRetriever('PYTESTID', input)
    assert getter.getAccessCode() == 'PYTESTCODE'

""" 
CHANGER TESTS 
"""
def test_changer_initMessageSplit():
    input = "TESTentryType, TESTaccountName, TESTinput, TESTcode"
    changer = LoginInfoChanger('PYTESTID', input)
    assert changer.entryType == 'TESTentryType'
    assert changer.accountName == 'TESTaccountName'
    assert changer.newInput == 'TESTinput'
    assert changer.accessCode == 'TESTcode'
    assert changer.tableName == 'userPYTESTID'

def test_changer_responseText():
    input = "TESTentryType, PYTESTaccountName, TESTinput, TESTcode"
    changer = LoginInfoChanger('PYTESTID', input)
    res = changer.responseText(True)
    assert res ==  "TESTentryType successfully changed for PYTESTaccountName"
    res = changer.responseText(False)
    assert res == "Data does not exist. If you wish to set your data, use the /pw-mgr-set command."

def test_changer_getAccessCode():
    input = " username, PYTESTaccountName, TESTinput, PYTESTCODE"
    changer = LoginInfoChanger('PYTESTID', input)
    assert changer.getAccessCode() == 'PYTESTCODE'

""" 
REMOVER TESTS 
"""
def test_remover_initMessageSplit():
    input = "TESTaccountName, TESTcode"
    remover = LoginInfoRemover('PYTESTID', input)
    assert remover.accountName == 'TESTaccountName'
    assert remover.accessCode == 'TESTcode'
    assert remover.tableName == 'userPYTESTID'

def test_remover_responseText():
    input = "TESTaccountName, TESTcode"
    remover = LoginInfoRemover('PYTESTID', input)
    res = remover.responseText(True)
    assert res ==  "All login data removed for TESTaccountName ."
    res = remover.responseText(False)
    assert res == "There is no data to remove. To set data, use the /pw-mgr-set command."

def test_removeInfo():
    test_conn = sqlite3.connect('billbot.db')
    test_cur = test_conn.cursor()
    dataToBeRemoved = test_cur.execute("INSERT INTO userPYTESTID VALUES(?, ?, ?)", ('remTESTACCOUNT', 'remTESTUSERNAME', 'remTESTPASSWORD'))
    test_conn.commit()
    input = "remTESTACCOUNT, PYTESTCODE"
    remover = LoginInfoRemover('PYTESTID', input)
    remover.removeInfo()
    query = "SELECT username FROM userPYTESTID WHERE accountName=?"
    res = test_cur.execute(query, ('remTESTACCOUNT',))
    row = res.fetchone()
    test_conn.close()
    assert row == None
    assert row != 'remTESTUSERNAME'

def test_remover_getAccessCode():
    input = "PYTESTaccountName, PYTESTCODE"
    remover = LoginInfoRemover('PYTESTID', input)
    assert remover.getAccessCode() == 'PYTESTCODE'

""" 
BOT USER MANAGER TESTS 
"""
def test_checkUserExists():
    botMngr = BotUserInfoManager()
    assert botMngr.checkUserExists('nonexistentID') == False
