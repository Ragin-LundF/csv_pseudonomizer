import mmap
import os

from tqdm import tqdm

import config


def full_filename(file: str, path='.'):
    return os.path.join(os.getcwd(), path, file)


def read_file_lines(input_file: str, path='.'):
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


def save_list_of_lines(output_file: str, data: list[str], mode='w', path='.'):
    total_processed_out = 0
    with open(full_filename(output_file, path=path), mode, encoding=config.csv_encoding, newline='') as fp:
        with tqdm(total=len(data), desc=f"writing {output_file}") as progress_bar_out:
            for line in data:
                total_processed_out += 1
                progress_bar_out.update(total_processed_out - progress_bar_out.n)
                fp.write(f"{line}\n")
    fp.close()


def delete_file(file: str, path='.'):
    os.remove(full_filename(file, path=path))
