import csv
import multiprocessing

from contextlib import closing
from faker import Faker
from tqdm import tqdm

# the amount of data will be records/number_of_threads...
number_of_threads = 6
records = 10_000_000
csv_file_name = "dummy.csv"
csv_headers = ["counterpartName", "counterpartIBAN", "counterpartAccountNo", "counterpartBIC", "accountNo",
               "purposeLine", "amount"]
fake = Faker('de_DE')


# function to generate a chunk of data
def join_csv_rows(row):
    row_list = []

    for i in tqdm(range(int(records / number_of_threads))):
        row_list.append({
            "counterpartName": counterpart_name(fake),
            "counterpartIBAN": fake.iban(),
            "counterpartAccountNo": fake.random_int(min=1000000, max=99999999),
            "counterpartBIC": fake.swift(length=11),
            "accountNo": fake.random_int(min=1000000, max=99999999),
            "purposeLine": fake.sentence(nb_words=5),
            "amount": fake.pricetag()
        })
    return row_list


# function  to generate csv data and file
def generate_dummy_data():
    with closing(multiprocessing.Pool()) as pool:
        print("Create data (progress per thread)...")
        joined_csv_rows = pool.imap_unordered(join_csv_rows, range(number_of_threads))

        with open(csv_file_name, 'wt') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=csv_headers)
            writer.writeheader()
            for row_list in joined_csv_rows:
                writer.writerows(row_list)


# returns a counterpart name as company or person name
def counterpart_name(fake):
    if fake.boolean(chance_of_getting_true=30):
        return fake.company()
    else:
        return fake.name()
