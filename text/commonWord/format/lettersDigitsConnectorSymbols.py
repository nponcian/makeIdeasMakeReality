import re

from text.commonWord.format import textFormatter

SYMBOLS_CONNECTING_WORDS = "-_'.&+"
SEPARATOR = " "

class LettersDigitsConnectorSymbols(textFormatter.TextFormatter):
    def __init__(self):
        super().__init__()

    def reconstruct(self, text):
        if not text: return text
        text = text.casefold()
        text = self.__removeNonConnectorSymbols(text)
        text = self.__stripConnectorSymbols(text)
        return text

    def __removeNonConnectorSymbols(self, text):
        return re.sub("[^\w" + re.escape(SYMBOLS_CONNECTING_WORDS) + "]", SEPARATOR, text)
        # or
        # filteredText = str()
        # for ch in text:
        #     if ch.isalnum() or ch in SYMBOLS_CONNECTING_WORDS:
        #         filteredText += ch
        #     else:
        #         filteredText += SEPARATOR
        # return filteredText

    def __stripConnectorSymbols(self, text):
        updatedText = str()
        for word in text.split():
            strippedWord = self.__stripNonAlNum(word)
            if len(strippedWord) > 0:
                updatedText += strippedWord + SEPARATOR
            # or using another logic via filter:
            # nonEmptyWords = list(filter(lambda word: len(word) > 0, words))
        return updatedText.rstrip()

    def __stripNonAlNum(self, word):
        # could be simplified to "if word.isalnum(): return word" but seems to be slower
        if len(word) <= 1: return word if word.isalnum() else ""

        # cannot use \w here as it includes _
        substr = re.search("[a-zA-Z0-9].*[a-zA-Z0-9]", word)
        return substr.group(0) if substr is not None else ""