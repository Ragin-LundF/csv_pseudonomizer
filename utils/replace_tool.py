import ahocorasick


class ReplaceUtils:
    """
    Replace utils class to efficient replace text with data from a dict.

    It uses the Aho Corasick algorithm to find keywords in the given phrase and replaces
    same with same things.

    If a dict is added, the tool automatically makes the final Trie for the given elements.
    In case that items are added step by step with the `add_item()` method, the `make()` method
    has to be called after all elements are added.
    """
    def __init__(self):
        self.automaton = ahocorasick.Automaton()

    def add_item(self, key: str, value: str):
        """
        Adds a single item to the Trie.

        :param key: Keyword to use for replacement
        :param value: Alternative, with which the keyword should be replaced
        :return: None
        """
        self.automaton.add_word(key, (key, value))

    def add_dict(self, dictionary: dict):
        """
        Add a full dict to the Trie.
        After the dict was applied, it executes `make()` automatically.
        The dict must have the following structure:

        {
            "key": "word which should replace the key",
            "another key": "another replacement"
        }

        :param dictionary:
        :return: None
        """
        for key in dictionary:
            self.add_item(key, dictionary.get(key)[0])
        self.make()

    def make(self):
        """
        Call this method after all items are added with `add_item()` method and before
        the `replace()` function should be executed.

        :return: None
        """
        self.automaton.make_automaton()

    def replace(self, element: str) -> str:
        """
        Replaces a keyword from the previous given dict or added item with the value.

        :param element:  The element that contains possible keywords to be replaced.
        :return: Replaced string
        """
        result = []
        words = element.split(' ')
        for i, word in enumerate(words):
            replaced = False
            for end, (key, value) in self.automaton.iter(word):
                result.append(word[:end - len(key) + 1] + value + word[end + 1:])
                replaced = True
            if not replaced:
                result.append(word)
        return ' '.join(result)
