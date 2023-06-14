import pytest
import sys
sys.path.append('../')
from zahmed2.src.translator import BillikenTranslator

def test_getStartLanguage():	
	testStringEnglish = 'Hello'
	testStringSpanish = 'Hola chica'
	testStringNone = 'Hola'
	translator = BillikenTranslator()
	assert 'es' == translator.getStartLanguage(testStringSpanish), "test failed"
	assert 'en' == translator.getStartLanguage(testStringEnglish), "test failed"
	# Low confidence will return none 
	assert None == translator.getStartLanguage(testStringNone), "test failed"


def test_getEndLanguage():
	testStringEnglish = 'English'
	testStringSpanish = 'Spanish'
	testStringNone = 'Gibberish'
	translator = BillikenTranslator()
	assert 'en' == translator.getEndLanguage(testStringEnglish), "test failed"
	assert 'es' == translator.getEndLanguage(testStringSpanish), "test failed"
	assert None == translator.getEndLanguage(testStringNone), "test failed"


def test_translateMessage():
	testMessage = 'Hi, how are you?'
	testStartLanguage = 'en'
	testEndLanguage = 'es'
	translator = BillikenTranslator()
	assert '¿Hola, cómo estás?' == translator.translateMessage(testMessage, testStartLanguage, testEndLanguage), "test failed"
	