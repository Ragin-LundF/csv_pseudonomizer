from pseudonomizer.global_dict import get_element, add_element


def pseudonomize_name(fake, element):
    replaced_name = get_element(element)
    if replaced_name is None:
        fake_name = fake.name()
        add_element(original=element, replaced=fake_name)
        return fake_name
    else:
        return replaced_name
