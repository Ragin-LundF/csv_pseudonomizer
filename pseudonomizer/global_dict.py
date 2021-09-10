import os
from dataclasses import make_dataclass

import pandas
import pyarrow as pa
import pyarrow.parquet as pq
from faker import Faker
from flashtext import KeywordProcessor

import config
from pseudonomizer.rules.person_names_only import company_detection_regexes
from utils.file_utils import read_file_lines

# global objects
ReplaceObj = make_dataclass("ReplaceObj", [("original", str), ("replaced", str)])
global_replace_dict_old = pandas.DataFrame([ReplaceObj(None, None)])
global_replace_dict = dict()
global_is_company_regexes = []
name_dictionary = {}
name_processor = KeywordProcessor()


def init():
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


def replace_names_in_element(element: str):
    return name_processor.replace_keywords(element)


def get_element(element: str):
    try:
        return ''.join(global_replace_dict[element])
    except KeyError:
        return None


def add_element(original: str, replaced: str):
    global global_replace_dict
    global_replace_dict[original] = replaced


def is_company_name(line: str):
    return global_is_company_regexes[0].search(line)


def save_mapping_data():
    # Store name dict
    save_mapping(name_dictionary, filename(config.mapping_file_name_names))
    # Store other mappings dict
    save_mapping(global_replace_dict, filename(config.mapping_file_name_dict))


def save_mapping(data: dict, file: str):
    table = pa.Table.from_pydict(data)
    pq.write_table(table, file)


def load_mapping_dict():
    if os.path.isfile(filename(config.mapping_file_name_dict)):
        table = pq.read_table(filename(config.mapping_file_name_dict))
        global global_replace_dict
        global_replace_dict = table.to_pydict()


def load_name_dict():
    if os.path.isfile(filename(config.mapping_file_name_names)):
        table = pq.read_table(filename(config.mapping_file_name_names))
        global name_dictionary
        name_dictionary = table.to_pydict()


def filename(name: str):
    return f"{name}.parquet"
