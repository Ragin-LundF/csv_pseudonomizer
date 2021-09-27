from pseudonomizer.purpose.pseudo_purpose import PurposePseudonomizer
from tests.test_base import BaseTest


class TestPurposePseudonomizer(BaseTest):
    __test__ = True

    def test_name_purpose_pseudonomize(self):
        name_person_1 = 'Max Müller'
        purpose = 'Billing Max Müller RG 123'

        result_name_replace = PurposePseudonomizer.pseudonomize(self.faker, name_person_1)
        result_purpose = PurposePseudonomizer.pseudonomize(self.faker, purpose)

        self.assertNotEqual(name_person_1, result_name_replace)
        self.assertNotEqual(purpose, result_purpose)
        self.assertTrue(result_name_replace in result_purpose)
        self.assertTrue(result_purpose.startswith('Billing '))
        self.assertTrue(result_purpose.endswith('RG 123'))

    def test_name_multiple_times(self):
        purpose = 'Max Müller Billing Max and Mrs. Müller'

        result_replace = PurposePseudonomizer.pseudonomize(self.faker, purpose)

        self.assertNotEqual(purpose, result_replace)
        self.assertTrue('Müller' not in result_replace)
        self.assertTrue('Max' not in result_replace)

    def test_iban_in_purpose(self):
        purpose = 'Max Müller DE12312312312312 ReNr'
        result_purpose_first = PurposePseudonomizer.pseudonomize(self.faker, purpose)
        result_purpose_second = PurposePseudonomizer.pseudonomize(self.faker, purpose)

        self.assertNotEqual(purpose, result_purpose_first)
        self.assertEqual(result_purpose_first, result_purpose_second)
