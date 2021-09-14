from pseudonomizer.iban.pseudo_iban import IbanPseudonomizer
from tests.test_base import BaseTest


class TestIbanPseudonomizer(BaseTest):
    __test__ = True

    def testIbanPseudonomize(self):
        iban_first = "DE1234567879"
        iban_second = "DE987654321"
        result_first = IbanPseudonomizer.pseudonomize(self.faker, iban_first)
        result_second = IbanPseudonomizer.pseudonomize(self.faker, iban_second)
        result_third = IbanPseudonomizer.pseudonomize(self.faker, iban_first)

        self.assertNotEqual(iban_first, result_first)
        self.assertNotEqual(result_first, result_second)
        self.assertEqual(result_first, result_third)
