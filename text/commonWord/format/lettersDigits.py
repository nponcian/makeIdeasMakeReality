import re

from text.commonWord.format import textFormatter

SEPARATOR = " "

class LettersDigits(textFormatter.TextFormatter):
    def __init__(self):
        super().__init__()

    def reconstruct(self, text):
        if not text: return text
        text = text.casefold()
        text = self.__retainLettersDigits(text)
        return text

    def __retainLettersDigits(self, text):
        return re.sub("[^a-zA-Z0-9]", SEPARATOR, text)