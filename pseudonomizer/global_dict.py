import logging
import os
import pickle
import re
from typing import Union, Optional

from faker import Faker

import config
from pseudonomizer.rules.company_regexes import company_detection_regexes
from utils.file_utils import read_file_lines
from utils.replace_tool import ReplaceUtils

# global objects
global_replace_dict = {}
global_is_company_regexes = []
name_dictionary = {}
name_replacer = ReplaceUtils()
iban_regex = re.compile(r'[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}')
email_regex = re.compile(r'\S+@\S+\.\S+')


def init(path='.'):
    """
    Initializes the global dictionary.
    It contains some `cached` data like names or IBANs to be able to replace the same with the same.
    If the mapping should be stored, it tries to read the mappings from the files into the memory.
    This helps to process different files one after another, but with the same replacements.

    For names, it uses the a Aho-Corasick algorithm to ensure a high performance in string replacements.

    :param path: Root path of the main.py
    :return: None
    """
    if config.save_mapping:
        logging.info("Loading existing mapping dictionary....")
        __load_mapping_dict()
        logging.info("Loading existing name dictionary....")
        __load_name_dict()
        logging.info("Loading done...")

    # initialize global is company regexes
    global global_is_company_regexes
    global_is_company_regexes = company_detection_regexes()

    # initialize global name dictionary
    global name_dictionary
    if not bool(name_dictionary):
        faker = Faker(config.fake_locale)
        first_names = read_file_lines('pseudonomizer/rules/firstnames.txt', path=path)
        last_names = read_file_lines('pseudonomizer/rules/lastnames.txt', path=path)

        # the following code ensures, that the same name is not generated by the faker for the original
        for firstname in first_names:
            original_firstname = firstname.decode(config.csv_encoding).strip()
            fake_firstname = faker.first_name()
            while fake_firstname == original_firstname:
                fake_firstname = faker.first_name()
            name_dictionary[original_firstname] = [fake_firstname]
        for lastname in last_names:
            original_lastname = lastname.decode(config.csv_encoding).strip()
            fake_lastname = faker.last_name()
            while fake_lastname == original_lastname:
                fake_lastname = faker.first_name()
            name_dictionary[original_lastname] = [fake_lastname]

    name_replacer.add_dict(name_dictionary)


def replace_names_in_element(element: str, replace_numbers=True) -> str:
    """
    Global replace method for names.
    It is more a helper method which uses the ReplacerUtils to replace the names.

    :param element: Column, which should be used to replace the name.
    :param replace_numbers: True if strings with numbers should also be replaced. Default is True.
    :return: Column with replaced name.
    """
    return name_replacer.replace(element, replace_numbers)


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


def contains_iban(element: str) -> Optional[str]:
    """
    Checks if an IBAN is existing.
    If yes, it returns the string for replacement.

    :param element:   Element to check
    :return: IBAN or None
    """
    iban_srch = iban_regex.search(element)
    if iban_srch is not None:
        return iban_srch.group(0)


def contains_email(element: str) -> Optional[str]:
    """
    Checks if an e-mail is existing.
    If yes, it returns the string for replacement.

    :param element:  Element to check
    :return: E-Mail or None
    """
    email_srch = email_regex.search(element)
    if email_srch is not None:
        return email_srch.group(0)


def save_mapping_data():
    """
    Save the mapping data to files.
    This method delegates to the save_mapping() method with all the dicts.

    :return: None
    """
    # Store name dict
    try:
        logging.info("Saving name mapping file...")
        __save_mapping(name_dictionary, __filename(config.mapping_file_name_names))
    except BaseException as bse:
        logging.error('Unable to save names dictionary.')
        logging.error(bse, exc_info=True)
    # Store other mappings dict
    try:
        logging.info("Saving global mapping file...")
        __save_mapping(global_replace_dict, __filename(config.mapping_file_name_dict))
    except BaseException as bse:
        logging.error('Unable to save mapping dictionary.')
        logging.error(bse, exc_info=True)


def __save_mapping(data: dict, file: str):
    """
    Save a mapping to the disk as pickle file.

    :param data: dict that should be stored.
    :param file: output filename
    :return: None
    """
    with open(file, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def __load_mapping_dict():
    """
    Read the mapping pickle file from disk and push it to the global_replace_dict.

    :return: None
    """
    if os.path.isfile(__filename(config.mapping_file_name_dict)):
        with open(__filename(config.mapping_file_name_dict), 'rb') as handle:
            global global_replace_dict
            global_replace_dict = pickle.load(handle)


def __load_name_dict():
    """
    Load the name pickle file and push it to the name dict.

    :return: None
    """
    if os.path.isfile(__filename(config.mapping_file_name_names)):
        with open(__filename(config.mapping_file_name_names), 'rb') as handle:
            global name_dictionary
            name_dictionary = pickle.load(handle)


def __filename(name: str) -> str:
    """
    Create the filename for the pickle files with extension.

    :param name: base name.
    :return: file name with extension
    """
    return f"{name}.pkl"
