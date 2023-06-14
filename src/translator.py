import googletrans
from googletrans import Translator

class BillikenTranslator(Translator):
    
    def getStartLanguage(self, message: str):
        '''
        Detects language of message and returns code used 
        by googletrans library up to 90% confidence
        '''
        detect = self.detect(message)
        if float(detect.confidence) < 0.9:
            return None
        else:
            return detect.lang


    def getEndLanguage(self, language: str):
        '''Searches googletrans dictionary of 
        {language code: language name} for match to input'''

        languages = googletrans.LANGUAGES
        for key in languages:
            if languages[key] == language.lower():
                return key
        return None


    def translateMessage(self, message:str, startLanguage:str, endLanguage:str):
        translated = self.translate(message, src=startLanguage, dest=endLanguage)
        return translated.text
