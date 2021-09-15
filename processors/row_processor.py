import importlib
from typing import Union

from faker import Faker

import config


def process_row(fake: Faker, row, with_header=False) -> Union[str, None]:
    """
    This method will be called to process a row of a CSV file.
    It ignores the header line by comparing the first element with the configuration
    definition.
    Each line will be split by the CSV separator from the config.

    :param fake: instance of the Faker to reuse the Faker once instantiated.
    :param row: the current row, which should be processed
    :param with_header: if true, the header is printed in the output file.
    :return: the processed line or None if the header line was not processed from the first split file
    """
    term = row.decode(config.csv_encoding).split(config.csv_separator)
    term = remove_leading_and_trailing_chars(term)

    if term[0] != config.csv_headers[0]:
        for pseudo_element in config.pseudo:
            idx_to_modify = get_column_id(pseudo_element.get('name'))
            if idx_to_modify is None:
                print(f"Unable to find element {pseudo_element.get('name')}")
                raise LookupError(f"Unable to find element {pseudo_element.get('name')}")
            module = importlib.import_module(pseudo_element.get('import'))
            cls = getattr(module, pseudo_element.get('class'))

            term[idx_to_modify] = cls.pseudonomize(fake, term[idx_to_modify])
    else:
        if not with_header:
            return None

    return ','.join(term)


def get_column_id(element: str) -> Union[int, None]:
    """
    Returns the index ID of the column.
    The structure of the CSV is defined in the configuration.

    :param element: Element for which the index is to be found.
    :return: The index or None, if it was not found.
    """
    idx = 0
    for col in config.csv_headers:
        if col == element:
            return idx
        else:
            idx += 1


def remove_leading_and_trailing_chars(column_array: list[str]) -> []:
    """
    Removes leading and trailing characters from the array.
    The config defines, which leading and trailing characters should be removed.

    :param column_array: Array to process
    :return: Striped array
    """
    new_column_array = []
    for column in column_array:
        column = column.lstrip(config.csv_remove_leading)
        column = column.rstrip(config.csv_remove_trailing)
        new_column_array.append(column)

    return new_column_array
