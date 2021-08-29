import config


def process_row(row):
    term = row.decode("utf-8").split(config.csv_separator)
    term[0] = "1"
    term[1] = "2"
    term[2] = "3"

    return ",".join(term)
