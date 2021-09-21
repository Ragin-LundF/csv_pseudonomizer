from pseudonomizer.numericid.pseudo_numericid import NumericIdPseudonomizer
from tests.test_base import BaseTest


class TestNumericIdPseudonomizer(BaseTest):
    __test__ = True

    def test_numericid_pseudonomize(self):
        id_1 = '1234567890'
        id_2 = '9234567890'

        result_first = NumericIdPseudonomizer.pseudonomize(self.faker, id_1)
        result_second = NumericIdPseudonomizer.pseudonomize(self.faker, id_2)
        result_third = NumericIdPseudonomizer.pseudonomize(self.faker, id_1)

        self.assertNotEqual(id_1, result_first)
        self.assertNotEqual(id_2, result_second)
        self.assertNotEqual(id_1, result_third)
        self.assertEqual(result_first, result_third)
