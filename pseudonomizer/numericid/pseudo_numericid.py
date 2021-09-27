import random

from faker import Faker

from pseudonomizer.global_dict import get_element, add_element
from pseudonomizer.pseudonomizer_interface import PseudonomizerInterface


class NumericIdPseudonomizer(PseudonomizerInterface):
    """
    This class pseudomizes numeric ids.
    Numeric IDs are always replaced with same numbers to ensure, that the pattern structure is kept.
    """

    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        replaced_id = get_element(element)
        if replaced_id is None:
            fake_id = str(random.randrange(1000000, 9999999999))
            add_element(original=element, replaced=fake_id)
            return fake_id
        else:
            return replaced_id
