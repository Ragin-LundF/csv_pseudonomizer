import config
import pseudonomizer


def process_row(fake, row):
    term = row.decode("utf-8").split(config.csv_separator)
    term[0] = "1"
    term[1] = "2"
    term[2] = "3"

    # todo
    for pseudo_element in config.pseudo:
        pseudo_config = pseudo_element.get()
        idx_to_modify = get_column_id(pseudo_config[0])
        method = getattr(pseudonomizer, pseudo_config[1])
        term[idx_to_modify] = method(fake, term[idx_to_modify])
    return ",".join(term)


def get_column_id(element):
    idx = 0
    for col in config.csv_headers:
        if col == element:
            return idx
        else:
            idx += 1
