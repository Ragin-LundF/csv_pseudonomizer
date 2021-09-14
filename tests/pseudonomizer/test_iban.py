import unittest

from faker import Faker

import config
from pseudonomizer.global_dict import init
from pseudonomizer.iban.pseudo_iban import IbanPseudonomizer


class TestIbanPseudonomizer(unittest.TestCase):
    def testIbanPseudonomize(self):
        init('../../')
        faker = Faker(config.fake_locale)
        iban_first = "DE1234567879"
        iban_second = "DE987654321"
        result_first = IbanPseudonomizer.pseudonomize(faker, iban_first)
        result_second = IbanPseudonomizer.pseudonomize(faker, iban_second)
        result_third = IbanPseudonomizer.pseudonomize(faker, iban_first)

        self.assertNotEqual(iban_first, result_first)
        self.assertNotEqual(result_first, result_second)
        self.assertEqual(result_first, result_third)


if __name__ == '__main__':
    unittest.main()