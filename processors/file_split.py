import csv
import glob
import os

from tqdm import tqdm

import config
from model.parameter_dc import Parameter


def split(input_file: str, number_of_chunks: int, output_path='.'):
    """
    Split a file into smaller chunks.
    Each new file contains the header of the original file.

    :param input_file: File to split.
    :param number_of_chunks: Number of chunks (lines).
    :param output_path: Optional output path, if the file should not stored in the main directory.
    """
    with open(input_file, newline='', encoding=config.csv_encoding) as csv_file_handler:
        chunk_file_name = os.path.splitext(input_file)[0] + config.split_file_template_trailing
        csv_reader = csv.reader(csv_file_handler, delimiter=config.csv_separator)
        current_chunk = 1
        output_file = output_file_name_for_split(chunk_file_name, current_chunk)

        current_out_writer = csv.writer(open(output_file, 'w', newline='', encoding=config.csv_encoding))
        current_limit = number_of_chunks

        headers = next(csv_reader)
        current_out_writer.writerow(headers)

        with tqdm(desc=f"writing {output_file} (lines)") as progress_bar_out:
            for i, row in enumerate(csv_reader):
                if i + 1 > current_limit:
                    current_chunk += 1
                    current_limit = number_of_chunks * current_chunk
                    current_out_path = output_file_name_for_split(
                        chunk_file_name,
                        current_chunk
                    )
                    current_out_writer = csv.writer(open(current_out_path, 'w', newline='', encoding=config.csv_encoding))
                    current_out_writer.writerow(headers)
                current_out_writer.writerow(row)


def output_file_name_for_split(chunk_file_name: str, chunk: int, output_path='.') -> str:
    """
    Generates the name of the output file name for the split file process.
    It adds numbers at the end of the file to have an ordered list.

    :param chunk_file_name: file name template for the chunks.
    :param chunk: current chunk number.
    :param output_path: optional path for the output file.
    :return: joined and template resolved filename.
    """
    return os.path.join(output_path, chunk_file_name % str(chunk).zfill(4))


def file_name_for_processing(params: Parameter) -> []:
    """
    Returns a list of files which should be processed.
    If it is in `processing split files` mode, it tries to detect the files.
    The single file mode returns the file as a list with one entry.

    :param params: Parameter dataclass which contains the filenames.
    :return: list of filename(s).
    """
    file_list = []
    if params.is_split_file:
        file_name_without_ext = os.path.splitext(params.input_file)[0]
        trailing_template = config.split_file_template_trailing.replace("%s", "*")
        file_list = glob.glob(file_name_without_ext + trailing_template)
    else:
        file_list.append(params.input_file)

    return file_list