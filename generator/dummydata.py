import csv
import multiprocessing
from contextlib import closing

from faker import Faker
from tqdm import tqdm

import config

# the amount of data will be records/number_of_threads...
fake = Faker(config.fake_locale)


def generate_dummy_data():
    """
    Function to generate CSV data and write it to a file.

    :return: None
    """
    with closing(multiprocessing.Pool()) as pool:
        print('Create data (progress per thread)...')
        joined_csv_rows = pool.imap_unordered(create_fake_csv_rows, range(config.generator_number_of_threads))

        with open(config.generator_csv_file_name, 'wt', encoding='utf-8', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=config.csv_headers)
            writer.writeheader()
            for row_list in joined_csv_rows:
                writer.writerows(row_list)


def create_fake_csv_rows(params) -> []:
    """
    Function to create a list of fake CSV rows.

    :param params: params (required for imap_unordered())
    :return: list of fake rows for CSV output
    """
    row_list = []

    for _ in tqdm(range(int(config.generator_records / config.generator_number_of_threads))):
        counterpart_name = generate_counterpart_name()
        row_list.append({
            'counterpartName': counterpart_name,
            'counterpartIBAN': fake.iban(),
            'counterpartAccountNo': fake.random_int(min=1000000, max=99999999),
            'counterpartBIC': fake.swift(length=11),
            'accountNo': fake.random_int(min=1000000, max=99999999),
            'purposeLine': generate_purpose_line(counterpart_name),
            'amount': fake.pricetag()
        })
    return row_list


def generate_counterpart_name() -> str:
    """
    Returns a counterpart name as company or person name.

    :return: A fake counterpart name, which is per default in 30% a company.
    """
    if fake.boolean(chance_of_getting_true=30):
        return fake.company()
    else:
        return fake.name()


def generate_purpose_line(name) -> str:
    """
    Generate a fake purpose line.

    :param name: to test, that the purpose name will also be replaced, a name can be given here.
    :return: a fake purpose line
    """
    if fake.boolean(chance_of_getting_true=10):
        return fake.sentence(nb_words=2) + " " + name
    else:
        return fake.sentence(nb_words=5)


def generate_first_names():
    """
    Generate a list of fake first names in the firstnames.txt file.

    :return: None
    """
    names = []
    for i in range(0, 30000):
        name = fake.first_name()
        if name not in names:
            names.append(name)
    from utils.file_utils import save_list_of_lines
    save_list_of_lines('pseudonomizer/rules/firstnames.txt', names)


def generate_last_names():
    """
    Generate a list of fake last names in the lastnames.txt file.

    :return: None
    """
    names = []
    for i in range(0, 30000):
        name = fake.last_name()
        if name not in names:
            names.append(name)
    from utils.file_utils import save_list_of_lines
    save_list_of_lines('pseudonomizer/rules/lastnames.txt', names)
