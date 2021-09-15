from faker import Faker

from pseudonomizer.global_dict import replace_names_in_element, is_company_name
from pseudonomizer.pseudonomizer_interface import PseudonomizerInterface


class NamePseudonomizer(PseudonomizerInterface):
    """
    This class pseudomizes the name if it is not a company.
    Companies are not under GDPR.
    Names are always replaced with same names to ensure, that the pattern structure is kept.
    """
    @staticmethod
    def pseudonomize(fake: Faker, element: str) -> str:
        if is_company_name(element):
            return element
        else:
            return replace_names_in_element(element)
