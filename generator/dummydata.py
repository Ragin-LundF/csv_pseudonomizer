import csv
import logging
import multiprocessing
import uuid
from contextlib import closing

from faker import Faker
from tqdm import tqdm

import config
from utils.csv_utils import CsvSemicolon

fake = Faker(config.fake_locale)


def generate_dummy_data() -> None:
    """
    Function to generate CSV data and write it to a file.

    :return: None
    """
    with closing(multiprocessing.Pool()) as pool:
        logging.info('Create data (progress per thread)...')
        joined_csv_rows = pool.imap_unordered(create_fake_csv_rows, range(config.generator_number_of_threads))

        with open(config.generator_csv_file_name, 'wt', encoding='utf-8', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=config.csv_headers, dialect=CsvSemicolon, quotechar='"', quoting=csv.QUOTE_ALL)
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
            'id': f'{fake.random_int(min=1000000, max=9999999999)}',
            'parentId': 'NULL',
            'bankBookingDate': f'{fake.date()}',
            'amount': f'{fake.pricetag()}',
            'purpose': f'{generate_purpose_line(counterpart_name)}',
            'swiftCode': 'NMSC',
            'counterpartName': f'{counterpart_name}',
            'counterpartIban': f'{fake.iban()}',
            'counterpartMandateReference': 'NULL',
            'counterpartCustomerReference': 'NULL',
            'counterpartAccountNumber': f'{fake.random_int(min=1000000000, max=9999999999)}',
            'counterpartBLZ': 'NULL',
            'counterpartBIC': f'{fake.swift(length=11)}',
            'end2endReference': 'NULL',
            'creditorID': 'NULL',
            'debitorID': 'NULL',
            'type': 'NULL',
            'typeCodeZka': 'NULL',
            'sepaPurposeCode': 'NULL',
            'accountCurrency': f'{fake.currency_code()}',
            'accountType': 'Checking',
            'balance': f'{fake.pricetag()}',
            'overdraft': f'{fake.pricetag()}',
            'overdraftLimit': f'{fake.pricetag()}',
            'availableFunds': f'{fake.pricetag()}',
            'accountNumber': f'{fake.random_int(min=1000000000, max=9999999999)}',
            'IBAN': f'{fake.iban()}',
            'balanceDate': f'{fake.date()}',
            'accountSeized': 'ok'
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


def generate_first_names() -> None:
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


def generate_last_names() -> None:
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
