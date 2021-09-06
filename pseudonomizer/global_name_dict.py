import pandas
import re

from utils.file_utils import read_file_lines

global_firstname_dict = pandas.DataFrame()
global_lastname_dict = pandas.DataFrame()
global_name_regex = []


def init():
    global global_firstname_dict
    first_names = read_file_lines('pseudonomizer/rules/firstnames.txt')
    global_firstname_dict = pandas.DataFrame(first_names)

    global global_lastname_dict
    last_names = read_file_lines('pseudonomizer/rules/lastnames.txt')
    global_lastname_dict = pandas.DataFrame(last_names)

    global global_name_regex
    names_regex = read_file_lines('pseudonomizer/rules/person_names_only.txt')
    for name_regex in names_regex:
        global_name_regex.append(re.compile(rf"{name_regex}"))


def is_company_name(line: str):
    return global_name_regex[0].match(line)
