from dataclasses import dataclass


@dataclass
class Parameter:
    input_file: str
    output_file: str
    is_split_file: bool = False
