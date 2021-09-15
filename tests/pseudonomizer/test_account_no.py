from pseudonomizer.accountno.pseudo_account_no import AccountNoPseudonomizer
from tests.test_base import BaseTest


class TestAccountNoPseudonomizer(BaseTest):
    __test__ = True

    def test_account_no_pseudonomize(self):
        account_no_1 = '1234567890'
        account_no_2 = '9234567890'

        result_first = AccountNoPseudonomizer.pseudonomize(self.faker, account_no_1)
        result_second = AccountNoPseudonomizer.pseudonomize(self.faker, account_no_2)
        result_third = AccountNoPseudonomizer.pseudonomize(self.faker, account_no_1)

        self.assertNotEqual(account_no_1, result_first)
        self.assertNotEqual(account_no_2, result_second)
        self.assertNotEqual(account_no_1, result_third)
        self.assertEqual(result_first, result_third)
