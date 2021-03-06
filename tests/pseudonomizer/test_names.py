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

    def test_name_multiple_times(self):
        purpose = 'Max Müller Billing Max and Mrs. Müller'

        result_replace = NamePseudonomizer.pseudonomize(self.faker, purpose)

        self.assertNotEqual(purpose, result_replace)
        self.assertTrue('Müller' not in result_replace)
        self.assertTrue('Max' not in result_replace)

    def test_replace_case_insensitive(self):
        name = 'mAx mAier krankenversicherung'
        result_name = NamePseudonomizer.pseudonomize(self.faker, name)

        self.assertNotEqual(name, result_name)

    def test_company_name(self):
        name = 'Max Müller GmbH'
        result_name = NamePseudonomizer.pseudonomize(self.faker, name)

        self.assertEqual(name, result_name)
