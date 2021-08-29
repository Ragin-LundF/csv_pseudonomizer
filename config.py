# Processor
csv_separator = ","
csv_headers = ["counterpartName", "counterpartIBAN", "counterpartAccountNo", "counterpartBIC", "accountNo",
               "purposeLine", "amount"]
fake_locale = "de_DE"
pseudo = [
    {
        "name": "counterpartName",
        "import": "pseudonomizer.pseudo_names",
        "function": "pseudonomize_name"
    }
]

# Dummy data generator
# --- generator: the amount of data will be records/number_of_threads...
generator_number_of_threads = 6
generator_records = 10_000
generator_csv_file_name = "dummy.csv"
