import logging
import os

from tqdm import tqdm

import config
from utils.file_utils import save_list_of_lines


def split(input_file: str, number_of_chunks: int, output_path='.') -> None:
    """
    Split a file into smaller chunks.
    Each new file contains the header of the original file.

    :param input_file: File to split.
    :param number_of_chunks: Number of chunks (lines).
    :param output_path: Optional output path, if the file should not stored in the main directory.
    """
    with open(input_file, 'rb') as csv_file_handler:
        chunk_file_name = os.path.splitext(input_file)[0] + config.split_file_template_trailing
        current_chunk = 1
        output_file = __output_file_name_for_split(chunk_file_name, current_chunk)
        current_limit = number_of_chunks

        headers = next(csv_file_handler).decode(config.csv_encoding).strip()

        with tqdm(desc=f"writing split data of {input_file} (lines)") as progress_bar_out:
            lines = []
            saved = False
            for i, row in enumerate(csv_file_handler):
                lines.append(row.decode(config.csv_encoding).strip())

                if i + 1 > current_limit:
                    logging.info(f"Save limit file {output_file}")
                    current_limit = number_of_chunks * (current_chunk + 1)
                    saved = True
                    current_chunk += 1
                    __save_chunk(current_chunk, chunk_file_name, lines, headers)
                    lines = []
                progress_bar_out.update(i)

            if not saved:
                logging.info(f"Save file {output_file}")
                __save_chunk(current_chunk, chunk_file_name, lines, headers)


def __save_chunk(current_chunk: int, chunk_file_name: str, lines: [], headers: str):
    current_out_path = __output_file_name_for_split(
        chunk_file_name,
        current_chunk - 1
    )
    lines.insert(0, headers)
    save_list_of_lines(current_out_path, lines)


def __output_file_name_for_split(chunk_file_name: str, chunk: int, output_path='.') -> str:
    """
    Generates the name of the output file name for the split file process.
    It adds numbers at the end of the file to have an ordered list.

    :param chunk_file_name: file name template for the chunks.
    :param chunk: current chunk number.
    :param output_path: optional path for the output file.
    :return: joined and template resolved filename.
    """
    return os.path.join(output_path, chunk_file_name % str(chunk).zfill(4))
