from pseudonomizer.names.pseudo_names import NamePseudonomizer
from tests.test_base import BaseTest


class TestNamePseudonomizer(BaseTest):
    __test__ = True

    def testNamePseudonomize(self):
        name_john_doe = "Max Doe"
        name_johanna_doe = "Suzanne Doe"
        result_first = NamePseudonomizer.pseudonomize(self.faker, name_john_doe)
        result_second = NamePseudonomizer.pseudonomize(self.faker, name_johanna_doe)
        result_third = NamePseudonomizer.pseudonomize(self.faker, name_john_doe)

        self.assertNotEqual(name_john_doe, result_first)
        self.assertNotEqual(name_johanna_doe, result_second)
        self.assertNotEqual(result_first, result_second)
        self.assertEqual(result_first, result_third)
