# Processor
csv_separator = ","

# Dummy data generator
# --- the amount of data will be records/number_of_threads...
number_of_threads = 6
records = 10_000_000
csv_file_name = "dummy.csv"
csv_headers = ["counterpartName", "counterpartIBAN", "counterpartAccountNo", "counterpartBIC", "accountNo",
               "purposeLine", "amount"]
fake_locale = "de_DE"

pseudo = [
    {"counterpartName": "pseudonomize_name"}
]
