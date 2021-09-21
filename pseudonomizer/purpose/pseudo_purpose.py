import re

from faker import Faker

from pseudonomizer.global_dict import replace_names_in_element, is_company_name, contains_iban, iban_regex
from pseudonomizer.iban.pseudo_iban import IbanPseudonomizer
from pseudonomizer.pseudonomizer_interface import PseudonomizerInterface


class PurposePseudonomizer(PseudonomizerInterface):
    """
    This class pseudomizes the name in a purpose line.
    This is independent of a company, because it is more tricky here to find everything correct.
    Names are always replaced with same names to ensure, that the pattern structure is kept.
    """
    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        iban = contains_iban(element)
        if iban is not None:
            new_iban = IbanPseudonomizer.pseudonomize(fake, iban)
            element = element.replace(iban, new_iban)

        return replace_names_in_element(element)
