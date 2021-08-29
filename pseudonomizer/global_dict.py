from dataclasses import make_dataclass

import pandas

ReplaceObj = make_dataclass("ReplaceObj", [("original", str), ("replaced", str)])
global_replace_dict = pandas.DataFrame([ReplaceObj("", "")])


def get_element(element):
    replaced_data = global_replace_dict[(global_replace_dict.original == element)]
    if replaced_data.empty:
        return None
    else:
        return replaced_data.replaced.values[0]


def add_element(original, replaced):
    global global_replace_dict
    global_replace_dict = global_replace_dict.append([ReplaceObj(original=original, replaced=replaced)])
