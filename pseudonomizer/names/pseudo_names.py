from faker import Faker

from pseudonomizer.global_dict import replace_names_in_element, is_company_name


def pseudonomize_name(fake: Faker, element: str):
    if is_company_name(element):
        return element
    else:
        return replace_names_in_element(element)
