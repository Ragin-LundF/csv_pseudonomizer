import csv

from faker import Faker


def generate_dummy_data():
    file_name = "dummy.csv"
    records = 52_000_000
    headers = ["counterpartName", "counterpartIBAN", "counterpartAccountNo", "counterpartBIC", "accountNo",
               "purposeLine", "amount"]
    fake = Faker('en_US')

    with open(file_name, 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            writer.writerow({
                "counterpartName": counterpart_name(fake),
                "counterpartIBAN": fake.iban(),
                "counterpartAccountNo": fake.name(),
                "counterpartBIC": fake.swift(length=11),
                "accountNo": fake.random_int(min=1000000, max=99999999),
                "purposeLine": fake.sentence(nb_words=5),
                "amount": fake.pricetag()
            })


def counterpart_name(fake):
    if fake.boolean(chance_of_getting_true=30):
        return fake.company()
    else:
        return fake.name()
