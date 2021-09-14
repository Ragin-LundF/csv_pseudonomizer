from tests.test_base import BaseTest
from utils.replace_tool import Replacer


class TestReplacerUtils(BaseTest):
    __test__ = True

    def testReplacer(self):
        str1 = "I found Max here"
        replacer = Replacer()
        replacer.add_item('Max', 'Gustav')
        replacer.replace(str1)
