import re


class Parser:
    """
    The abstract class for text parsing. Allows for intuitive parsing of text in one run.

    The class contains protected helper methods for parsing text

    Attributes
    ----------
    text : str
        the text that will be parsed

    Methods
    -------
    _get_text_till_character(regex: str)
        Gets text until a character matches the regex passed
    """

    def __init__(self, text: str):
        """
        Initializes the parser state. Sets text _cursor to 0

        :param text: the text that will be parsed
        """

        self.text = text
        self._cursor = 0

    def _get_text_till_character(self, regex) -> str:
        """
        Advances the cursor till a certain regex match

        :param regex: the regex to match
        :return: the string up till the character
        """

        res = Parser.__get_text_till_character(self.text, self._cursor, regex)
        self._cursor = res[1]
        return res[0]

    def _pop(self):
        """
        Gives current cursor data and advances it

        :return: the current character at cursor location
        """

        res = Parser.__pop(self.text, self._cursor)
        self._cursor = res[1]
        return res[0]

    def _peek(self):
        """
        View the character at the next cursor location

        :return: the character at the next cursor location
        """

        return Parser.__peek(self.text, self._cursor)

    @staticmethod
    def __get_text_till_character(text: str, cursor: int, regex: str) -> (str, int):
        """
        Advances the cursor till a certain regex match
        Static method for general usage of the class

        :param text the text to use
        :param cursor the cursor, location in text
        :param regex: the regex to match
        :return: the string up till the character
        """

        txt = ""
        while not bool(re.match(regex, text[cursor])):
            pop = Parser.__pop(text, cursor)
            txt += pop[0]
            cursor = pop[1]
            if cursor + 1 > len(text):
                break
        cursor += 1
        return txt, cursor

    @staticmethod
    def __pop(text: str, cursor: int) -> (str, int):
        """
        Gives current cursor data and advances it

        :param text the text to use
        :param cursor the cursor, location in text
        :return: the current character at cursor location
        """

        txt = text[cursor]
        cursor += 1
        return txt, cursor

    @staticmethod
    def __peek(text: str, cursor: int) -> str:
        """
        View the character at the next cursor location

        :param text the text to use
        :param cursor the cursor, location in text
        :return: the character at the next cursor location
        """

        return text[cursor + 1]
