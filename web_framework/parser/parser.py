import re


class Parser:
    def __init__(self, text: str):
        self.text = text
        self.cursor = 0

    def _get_text_till_character(self, regex):
        res = Parser.__get_text_till_character(self.text, self.cursor, regex)
        self.cursor = res[1]
        return res[0]

    def _pop(self):
        res = Parser.__pop(self.text, self.cursor)
        self.cursor = res[1]
        return res[0]

    def _peek(self):
        return Parser.__peek(self.text, self.cursor)

    @staticmethod
    def __get_text_till_character(text: str, cursor: int, regex: str) -> (str, int):
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
        txt = text[cursor]
        cursor += 1
        return txt, cursor

    @staticmethod
    def __peek(text: str, cursor: int) -> str:
        return text[cursor + 1]
