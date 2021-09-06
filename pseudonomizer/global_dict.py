import os
from dataclasses import make_dataclass

import pandas
import pyarrow as pa
import pyarrow.parquet as pq

import config

ReplaceObj = make_dataclass("ReplaceObj", [("original", str), ("replaced", str)])
global_replace_dict = pandas.DataFrame([ReplaceObj(None, None)])


def get_element(element):
    replaced_data = global_replace_dict[(global_replace_dict.original == element)]
    if replaced_data.empty:
        return None
    else:
        return replaced_data.replaced.values[0]


def add_element(original, replaced):
    global global_replace_dict
    global_replace_dict = global_replace_dict.append([ReplaceObj(original=original, replaced=replaced)])


def save_dataframe():
    table = pa.Table.from_pandas(global_replace_dict)
    pq.write_table(table, config.mapping_file_name)


def load_dataframe():
    if os.path.isfile(config.mapping_file_name):
        table = pq.read_table(config.mapping_file_name)
        global global_replace_dict
        global_replace_dict = table.to_pandas()
