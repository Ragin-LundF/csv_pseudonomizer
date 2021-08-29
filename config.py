# Processor
# -- Separator for the CSV file
csv_separator = ","
# -- Headers of the target CSV file. This is also used for the dummy file.
csv_headers = ["counterpartName", "counterpartIBAN", "counterpartAccountNo", "counterpartBIC", "accountNo",
               "purposeLine", "amount"]
# -- Locale for the data (impacts the locale of the Fake library)
fake_locale = "de_DE"

# -- configuration for the pseudonomization
pseudo = [
    {
        "name": "counterpartName",
        "import": "pseudonomizer.pseudo_names",
        "function": "pseudonomize_name"
    },
    {
        "name": "counterpartIBAN",
        "import": "pseudonomizer.pseudo_iban",
        "function": "pseudonomize_iban"
    }
]

# Dummy data generator
# --- generator: the amount of data will be records/number_of_threads...
generator_number_of_threads = 6
generator_records = 10_000
generator_csv_file_name = "dummy.csv"
