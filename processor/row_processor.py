import importlib

from faker import Faker

import config


def process_row(fake: Faker, row, with_header=False):
    term = row.decode(config.csv_encoding).split(config.csv_separator)
    term = remove_leading_and_trailing_chars(term)

    if term[0] != config.csv_headers[0]:
        for pseudo_element in config.pseudo:
            idx_to_modify = get_column_id(pseudo_element.get('name'))
            if idx_to_modify is None:
                print(f"Unable to find element {pseudo_element.get('name')}")
                raise LookupError(f"Unable to find element {pseudo_element.get('name')}")
            module = importlib.import_module(pseudo_element.get('import'))
            method_to_call = getattr(module, pseudo_element.get('function'))

            term[idx_to_modify] = method_to_call(fake, term[idx_to_modify])
    else:
        if not with_header:
            return None

    return ",".join(term)


def get_column_id(element: str):
    idx = 0
    for col in config.csv_headers:
        if col == element:
            return idx
        else:
            idx += 1


def remove_leading_and_trailing_chars(column_array: list[str]):
    new_column_array = []
    for column in column_array:
        column = column.lstrip(config.csv_remove_leading)
        column = column.rstrip(config.csv_remove_trailing)
        new_column_array.append(column)

    return new_column_array
