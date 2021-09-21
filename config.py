# Processor
# -- Separator for the CSV file
import logging

# -- Separator of the CSV columns
csv_separator = '"";""'
# -- CSV leading chars for the first column if the data uses not only one separator character
csv_column_leading_chars_first = '""'
# -- CSV trailing chars for the last column if the data uses not only one separator character
csv_column_trailing_chars_end = '""'
# -- Defines leading characters, which should be removed from the columns
csv_remove_leading = '"'
# -- Defines trailing characters, which should be removed from the columns
csv_remove_trailing = '"'
# -- Headers of the target CSV file. This is also used for the dummy file.
csv_headers = [
    'id',
    'parentId',
    'bankBookingDate',
    'amount',
    'purpose',
    'swiftCode',
    'counterpartName',
    'counterpartIban',
    'counterpartMandateReference',
    'counterpartCustomerReference',
    'counterpartAccountNumber',
    'counterpartBLZ',
    'counterpartBIC',
    'end2endReference',
    'creditorID',
    'debitorID',
    'type',
    'typeCodeZka',
    'sepaPurposeCode',
    'accountCurrency',
    'accountType',
    'balance',
    'overdraft',
    'overdraftLimit',
    'availableFunds',
    'accountNumber',
    'IBAN',
    'balanceDate',
    'accountSeized'
]

csv_headers_remove_in_target = [
    'id',
    'parentId'
]

# -- CSV file encoding
csv_encoding = 'utf-8'
# -- Locale for the data (impacts the locale of the Fake library)
fake_locale = 'de_DE'

# -- Save the mapping as parquet file and reuse the existing one
save_mapping = True

# -- Mapping file names
mapping_file_name_dict = 'mapping_dict'
mapping_file_name_names = 'mapping_names'

# -- configuration for the pseudonomization
pseudo = [
    {
        'name': 'id',
        'import': 'pseudonomizer.numericid.pseudo_numericid',
        'class': 'NumericIdPseudonomizer'
    },
    {
        'name': 'counterpartName',
        'import': 'pseudonomizer.names.pseudo_names',
        'class': 'NamePseudonomizer'
    },
    {
        'name': 'purpose',
        'import': 'pseudonomizer.purpose.pseudo_purpose',
        'class': 'PurposePseudonomizer'
    },
    {
        'name': 'IBAN',
        'import': 'pseudonomizer.iban.pseudo_iban',
        'class': 'IbanPseudonomizer'
    },
    {
        'name': 'counterpartIban',
        'import': 'pseudonomizer.iban.pseudo_iban',
        'class': 'IbanPseudonomizer'
    },
    {
        'name': 'accountNumber',
        'import': 'pseudonomizer.accountno.pseudo_account_no',
        'class': 'AccountNoPseudonomizer'
    },
    {
        'name': 'counterpartAccountNumber',
        'import': 'pseudonomizer.accountno.pseudo_account_no',
        'class': 'AccountNoPseudonomizer'
    }
]

# Dummy data generator
# --- generator: the amount of data will be records/number_of_threads...
generator_number_of_threads = 6
generator_records = 100_000
generator_csv_file_name = 'dummy.csv'
split_file_template_trailing = '_chunk_%s.csv'

# Logging
logging.basicConfig(level=logging.INFO)
