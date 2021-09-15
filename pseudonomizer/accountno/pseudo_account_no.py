import random

from faker import Faker

from pseudonomizer.global_dict import get_element, add_element
from pseudonomizer.pseudonomizer_interface import PseudonomizerInterface


class AccountNoPseudonomizer(PseudonomizerInterface):
    """
    This class pseudomizes the account number.
    Account numbers are always replaced with same numbers to ensure, that the pattern structure is kept.
    """
    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        replaced_account_no = get_element(element)
        if replaced_account_no is None:
            fake_account_no = str(random.randrange(100000000, 9999999999))
            add_element(original=element, replaced=fake_account_no)
            return fake_account_no
        else:
            return replaced_account_no
