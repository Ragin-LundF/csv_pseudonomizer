import importlib

import config


def process_row(fake, row):
    term = row.decode("utf-8").split(config.csv_separator)

    if term[0] != config.csv_headers[0]:
        for pseudo_element in config.pseudo:
            idx_to_modify = get_column_id(pseudo_element.get('name'))
            if idx_to_modify is None:
                print(f"Unable to find element {pseudo_element.get('name')}")
                raise LookupError(f"Unable to find element {pseudo_element.get('name')}")
            module = importlib.import_module(pseudo_element.get('import'))
            method_to_call = getattr(module, pseudo_element.get('function'))

            term[idx_to_modify] = method_to_call(fake, term[idx_to_modify])
    return ",".join(term)


def get_column_id(element):
    idx = 0
    for col in config.csv_headers:
        if col == element:
            return idx
        else:
            idx += 1
