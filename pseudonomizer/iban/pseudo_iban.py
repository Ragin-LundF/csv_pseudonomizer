from faker import Faker

from pseudonomizer.global_dict import get_element, add_element
from pseudonomizer.pseudonomizer_interface import PseudonomizerInterface


class IbanPseudonomizer(PseudonomizerInterface):
    """
    This class pseudomizes the IBAN.
    IBANs are always replaced with same IBANs to ensure, that the pattern structure is kept.
    """

    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        replaced_iban = get_element(element)
        if replaced_iban is None:
            fake_iban = fake.iban()
            add_element(original=element, replaced=fake_iban)
            return fake_iban
        else:
            return replaced_iban
