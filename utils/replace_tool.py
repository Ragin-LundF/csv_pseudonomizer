import re

import ahocorasick

import config


class ReplaceUtils:
    number_regex = re.compile(r'([0-9])')

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

    def add_item(self, key: str, value: str) -> None:
        """
        Adds a single item to the Trie.

        :param key: Keyword to use for replacement
        :param value: Alternative, with which the keyword should be replaced
        :return: None
        """
        self.automaton.add_word(key.lower(), (key.lower(), value))

    def add_dict(self, dictionary: dict) -> None:
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

    def make(self) -> None:
        """
        Call this method after all items are added with `add_item()` method and before
        the `replace()` function should be executed.

        :return: None
        """
        self.automaton.make_automaton()

    def replace(self, element: str, replace_alphanumeric=True) -> str:
        """
        Replaces a keyword from the previous given dict or added item with the value.

        :param element:  The element that contains possible keywords to be replaced.
        :param replace_alphanumeric: True if strings with numbers should also be replaced. Default is True.
        :return: Replaced string
        """
        result = []
        words = element.split(' ')
        for i, word in enumerate(words):
            replaced = False

            if not replace_alphanumeric and self.__contains_number(word):
                pass
            else:
                word_low = word.lower()
                for end, (key, value) in self.automaton.iter(word_low):
                    if config.replace_purpose_names_with is not None and len(config.replace_purpose_names_with) > 0:
                        result.append(config.replace_purpose_names_with)
                        replaced = True
                        break
                    if not config.map_only_starting_keyword:
                        result.append(self.__tag_replacement(word[:end - len(key) + 1] + value + word[end + 1:]))
                        replaced = True
                        break
                    elif end - len(key) + 1 == 0:
                        result.append(self.__tag_replacement(value))
                        replaced = True
                        break
            if not replaced:
                result.append(word)
        return ' '.join(result)

    def __tag_replacement(self, element: str) -> str:
        tag_start = ''
        tag_end = ''
        if config.tag_replaced_name_with is not None and len(config.tag_replaced_name_with) > 0:
            tag_start = f'{config.tag_replaced_name_with}{config.tag_replaced_name_before}'
            tag_end = f'{config.tag_replaced_name_after}'
        return f'{tag_start}{element}{tag_end}'

    def __contains_number(self, element: str) -> bool:
        """
        Checks if string contains numbers

        :param element:  Element to check
        :return: True = number or False = no number
        """
        number_srch = self.number_regex.search(element)
        return number_srch is not None
