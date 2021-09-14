import os
from dataclasses import make_dataclass
from typing import Union

import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker
from flashtext import KeywordProcessor

import config
from pseudonomizer.rules.company_regexes import company_detection_regexes
from utils.file_utils import read_file_lines

# global objects
ReplaceObj = make_dataclass("ReplaceObj", [("original", str), ("replaced", str)])
global_replace_dict = dict()
global_is_company_regexes = []
name_dictionary = {}
name_processor = KeywordProcessor()


def init():
    """
    Initializes the global dictionary.
    It contains some `cached` data like names or IBANs to be able to replace the same with the same.
    If the mapping should be stored, it tries to read the mappings from the files into the memory.
    This helps to process different files one after another, but with the same replacements.

    For names, it uses the KeywordProcessor from flashtext to ensure a high performance in string replacements.

    :return: None
    """
    if config.save_mapping:
        print("Loading existing mapping dictionary....")
        load_mapping_dict()
        print("Loading existing name dictionary....")
        load_name_dict()
        print("Loading done...")

    # initialize global is company regexes
    global global_is_company_regexes
    global_is_company_regexes = company_detection_regexes()

    # initialize global name dictionary
    global name_dictionary
    if not bool(name_dictionary):
        faker = Faker(config.fake_locale)
        first_names = read_file_lines('pseudonomizer/rules/firstnames.txt')
        last_names = read_file_lines('pseudonomizer/rules/lastnames.txt')

        for firstname in first_names:
            name_dictionary[firstname.decode(config.csv_encoding).strip()] = [faker.first_name()]
        for lastname in last_names:
            name_dictionary[lastname.decode(config.csv_encoding).strip()] = [faker.last_name()]

    name_processor.add_keywords_from_dict(name_dictionary)


def replace_names_in_element(element: str) -> str:
    """
    Global replace method for names.
    It is more a helper method which uses the flashtext KeywordProcessor to replace the names.

    :param element: Column, which should be used to replace the name.
    :return: Column with replaced name.
    """
    return name_processor.replace_keywords(element)


def get_element(element: str) -> Union[str, None]:
    """
    Return the cached replacement of an element (like IBAN).
    If nothing was found, it returns None.

    :param element: Element key of the cache (e.g. IBAN).
    :return: The mapped element from the cache or None if it was never cached.
    """
    try:
        return ''.join(global_replace_dict[element])
    except KeyError:
        return None


def add_element(original: str, replaced: str):
    """
    Add an element to the global cache.

    :param original: Original value (key).
    :param replaced: New, replaced value (value).
    :return: None
    """
    global global_replace_dict
    global_replace_dict[original] = replaced


def is_company_name(element: str) -> bool:
    """
    Helper method to check, if there is a company name inside the element.

    :param element: Element to check.
    :return: True if it is a company, False, if not.
    """
    return global_is_company_regexes[0].search(element)


def save_mapping_data():
    """
    Save the mapping data to files.
    This method delegates to the save_mapping() method with all the dicts.

    :return: None
    """
    # Store name dict
    save_mapping(name_dictionary, filename(config.mapping_file_name_names))
    # Store other mappings dict
    save_mapping(global_replace_dict, filename(config.mapping_file_name_dict))


def save_mapping(data: dict, file: str):
    """
    Save a mapping to the disk as parquet file.

    :param data: dict that should be stored.
    :param file: output filename
    :return: None
    """
    table = pa.Table.from_pydict(data)
    pq.write_table(table, file)


def load_mapping_dict():
    """
    Read the mapping parquet file from disk and push it to the global_replace_dict.

    :return: None
    """
    if os.path.isfile(filename(config.mapping_file_name_dict)):
        table = pq.read_table(filename(config.mapping_file_name_dict))
        global global_replace_dict
        global_replace_dict = table.to_pydict()


def load_name_dict():
    """
    Load the name parquet file and push it to the name dict.

    :return: None
    """
    if os.path.isfile(filename(config.mapping_file_name_names)):
        table = pq.read_table(filename(config.mapping_file_name_names))
        global name_dictionary
        name_dictionary = table.to_pydict()


def filename(name: str) -> str:
    """
    Create the filename for the parquet files with extension.

    :param name: base name.
    :return: file name with extension
    """
    return f"{name}.parquet"
