import re

from faker import Faker

from pseudonomizer.global_dict import replace_names_in_element, contains_iban, contains_email, get_element
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
        # IBAN in purpose
        iban = contains_iban(element)
        if iban is not None:
            new_iban = IbanPseudonomizer.pseudonomize(fake, iban)
            element = element.replace(iban, new_iban)

        # e-mail in purpose
        email = contains_email(element)
        if email is not None:
            element = element.replace(email, '__deleted_email__')

        element = replace_names_in_element(element, replace_alphanumeric=False)
        return PurposePseudonomizer.replace_words_and_account_no(element)

    @staticmethod
    def replace_words_and_account_no(element: str):
        words = element.split(' ')
        result = []
        for word in words:
            if word.isnumeric():
                replaced_numbers = get_element(word)
                if replaced_numbers is not None:
                    result.append(replaced_numbers)
                else:
                    result.append(word)
            else:
                result.append(word)
        return ' '.join(result)
