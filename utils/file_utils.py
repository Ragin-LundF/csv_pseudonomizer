import glob
import mmap
import os

from tqdm import tqdm

import config
from model.parameter_dc import Parameter


def full_filename(file: str, path='.') -> str:
    """
    Return the full file with path.

    :param file: name of the file
    :param path: path of the file
    :return: joined full path and filename
    """
    return os.path.join(os.getcwd(), path, file)


def read_file_lines(input_file: str, path='.') -> []:
    """
    Read lines of a file and returns them as an array.

    :param input_file: filename of the file to read
    :param path:  optional path
    :return: array of lines
    """
    result = []
    with open(full_filename(input_file, path=path), 'r+b') as fp:
        # map the entire file into memory, normally much faster than buffered i/o
        mm = mmap.mmap(fp.fileno(), 0)
        # iterate over the block, until next newline
        for line in iter(mm.readline, b""):
            result.append(line)
        mm.close()
    fp.close()

    return result


def save_list_of_lines(output_file: str, data: list[str], mode='w', path='.') -> None:
    """
    Save list of strings to a file.

    :param output_file: Filename of the output file
    :param data: Array with data to save
    :param mode: Mode for opening the file (default is `w`)
    :param path: Optional path for the output file
    :return: None
    """
    total_processed_out = 0
    with open(full_filename(output_file, path=path), mode, encoding=config.csv_encoding, newline='') as fp:
        with tqdm(total=len(data), desc=f"writing {output_file}") as progress_bar_out:
            for line in data:
                total_processed_out += 1
                progress_bar_out.update(total_processed_out - progress_bar_out.n)
                fp.write(f"{line}\n")
    fp.close()


def delete_file(file: str, path='.') -> None:
    """
    Delete a file.

    :param file: Filename
    :param path: Optional path
    :return: None
    """
    os.remove(full_filename(file, path=path))


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
        trailing_template = config.split_file_template_trailing.replace('%s', '*')
        file_list = glob.glob(file_name_without_ext + trailing_template)
    else:
        file_list.append(params.input_file)

    return file_list
