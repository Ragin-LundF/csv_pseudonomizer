from pseudonomizer.names.pseudo_names import NamePseudonomizer
from tests.test_base import BaseTest


class TestNamePseudonomizer(BaseTest):
    __test__ = True

    def test_name_pseudonomize(self):
        name_person_1 = 'Max Müller'
        name_person_2 = 'Suzanne Steinberg'

        result_first = NamePseudonomizer.pseudonomize(self.faker, name_person_1)
        result_second = NamePseudonomizer.pseudonomize(self.faker, name_person_2)
        result_third = NamePseudonomizer.pseudonomize(self.faker, name_person_1)

        self.assertNotEqual(name_person_1, result_first)
        self.assertNotEqual(name_person_2, result_second)
        self.assertNotEqual(result_first, result_second)
        self.assertEqual(result_first, result_third)

    def test_name_purpose_pseudonomize(self):
        name_person_1 = 'Max Müller'
        purpose = 'Billing Max Müller RG 123'

        result_name_replace = NamePseudonomizer.pseudonomize(self.faker, name_person_1)
        result_purpose = NamePseudonomizer.pseudonomize(self.faker, purpose)

        self.assertNotEqual(name_person_1, result_name_replace)
        self.assertNotEqual(purpose, result_purpose)
        self.assertTrue(result_name_replace in result_purpose)
        self.assertTrue(result_purpose.startswith('Billing '))
        self.assertTrue(result_purpose.endswith('RG 123'))

    def test_company_name(self):
        name = 'Max Müller GmbH'
        result_name = NamePseudonomizer.pseudonomize(self.faker, name)

        self.assertEqual(name, result_name)
