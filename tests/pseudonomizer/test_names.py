import unittest

from faker import Faker

import config
from pseudonomizer.global_dict import init
from pseudonomizer.names.pseudo_names import NamePseudonomizer


class TestNamePseudonomizer(unittest.TestCase):
    def testNamePseudonomize(self):
        init('../../')
        faker = Faker(config.fake_locale)
        name_john_doe = "John Doe"
        name_johanna_doe = "Johanna Doe"
        result_first = NamePseudonomizer.pseudonomize(faker, name_john_doe)
        result_second = NamePseudonomizer.pseudonomize(faker, name_john_doe)
        result_third = NamePseudonomizer.pseudonomize(faker, name_john_doe)

        self.assertNotEqual(name_john_doe, result_first)
        self.assertEqual(result_first, result_second)
        self.assertNotEqual(name_johanna_doe, result_third)
        self.assertEqual(result_first, result_third)


if __name__ == '__main__':
    unittest.main()