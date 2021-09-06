from faker import Faker

from pseudonomizer.global_dict import get_element, add_element
from pseudonomizer.global_name_dict import is_company_name


def pseudonomize_name(fake: Faker, element: str):
    if is_company_name(element):
        return element
    elif should_be_removed:
        return "DELETED DATA"
    else:
        replaced_name = get_element(element)
        if replaced_name is None:
            fake_name = fake.name()
            add_element(original=element, replaced=fake_name)
            return fake_name
        else:
            return replaced_name
