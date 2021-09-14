from dataclasses import dataclass


@dataclass
class Parameter:
    """
    Parameter class to transport all data from the main.py into the methods.
    """
    input_file: str
    output_file: str
    is_split_file: bool = False
