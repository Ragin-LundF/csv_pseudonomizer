import ahocorasick


class Replacer:
    def __init__(self):
        self.automaton = ahocorasick.Automaton()

    def add_item(self, key: str, value: str):
        self.automaton.add_word(key, (key, value))

    def add_dict(self, dictionary: dict):
        for key in dictionary:
            self.add_item(key, dictionary.get(key)[0])
        self.make()

    def make(self):
        self.automaton.make_automaton()

    def replace(self, column: str) -> str:
        for end, (key, value) in self.automaton.iter(column):
            return column[:end - len(key) + 1] + value + column[end + 1:]
        return column