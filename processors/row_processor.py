import importlib
import logging
from typing import Optional

from faker import Faker

import config


def process_row(fake: Faker, row, with_header=False) -> Optional[str]:
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
    term = __remove_leading_and_trailing_chars(term)

    if term[0] != config.csv_headers[0]:
        for pseudo_element in config.pseudo:
            idx_to_modify = __get_column_id(pseudo_element.get('name'))
            if idx_to_modify is None:
                logging.error(f"Unable to find element {pseudo_element.get('name')}")
                raise LookupError(f"Unable to find element {pseudo_element.get('name')}")
            module = importlib.import_module(pseudo_element.get('import'))
            cls = getattr(module, pseudo_element.get('class'))

            term[idx_to_modify] = cls.pseudonomize(fake, str(term[idx_to_modify]))
    else:
        if not with_header:
            return None

    __add_leading_and_trailing_chars(term)
    return config.csv_separator.join(__remove_not_required_columns(term))


def __remove_not_required_columns(term: []) -> []:
    if len(config.csv_headers_remove_in_target) > 0:
        headers = list(config.csv_headers)
        for col_to_remove in config.csv_headers_remove_in_target:
            idx_to_remove = __get_column_id_with_header(col_to_remove, headers)
            term.pop(idx_to_remove)
            headers.pop(idx_to_remove)

    return term


def __get_column_id(element: str) -> Optional[int]:
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


def __get_column_id_with_header(element: str, headers: []) -> Optional[int]:
    """
    Returns the index ID of the column.
    The structure of the CSV is defined in the configuration.

    :param element: Element for which the index is to be found.
    :param headers: Headers
    :return: The index or None, if it was not found.
    """
    idx = 0
    for col in headers:
        if col == element:
            return idx
        else:
            idx += 1


def __remove_leading_and_trailing_chars(column_list: []) -> []:
    """
    Removes leading and trailing characters from the array.
    The config defines, which leading and trailing characters should be removed.

    :param column_list: Array to process
    :return: Striped array
    """
    new_column_list = []
    for column in column_list:
        column = column.lstrip(config.csv_remove_leading)
        column = column.rstrip(config.csv_remove_trailing)
        new_column_list.append(column)

    return new_column_list


def __add_leading_and_trailing_chars(column_list: []) -> None:
    """
    Add leading characters to the first column and trailing to the last column if
    the CSV uses more than one character as separator.
    E.g. ""Col1"";""Col2""

    :param column_list: Array to process
    :return: None
    """
    if len(column_list) > 0:
        if len(config.csv_column_leading_chars_first) > 0:
            column_list[0] = f"{config.csv_column_leading_chars_first}{column_list[0]}"

        if len(config.csv_column_trailing_chars_end) > 0:
            column_list[
                len(column_list) - 1] = f"{column_list[len(column_list) - 1]}{config.csv_column_trailing_chars_end}"
