from faker import Faker

from pseudonomizer.global_dict import get_element, add_element


def pseudonomize_iban(fake: Faker, element: str):
    replaced_iban = get_element(element)
    if replaced_iban is None:
        fake_iban = fake.iban()
        add_element(original=element, replaced=fake_iban)
        return fake_iban
    else:
        return replaced_iban
