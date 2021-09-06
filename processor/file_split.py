import csv
import os

from tqdm import tqdm

import config


def split(input_file: str, number_of_chunks: int, output_path='.'):
    with open(input_file, newline='', encoding=config.csv_encoding) as csv_file_handler:
        chunk_file_name = os.path.splitext(input_file)[0] + "_chunk_%s.csv"
        csv_reader = csv.reader(csv_file_handler, delimiter=config.csv_separator)
        current_chunk = 1
        output_file = output_file_name(chunk_file_name, current_chunk)

        current_out_writer = csv.writer(open(output_file, 'w', newline='', encoding=config.csv_encoding))
        current_limit = number_of_chunks

        headers = next(csv_reader)
        current_out_writer.writerow(headers)

        with tqdm(desc=f"writing {output_file} (lines)") as progress_bar_out:
            for i, row in enumerate(csv_reader):
                if i + 1 > current_limit:
                    current_chunk += 1
                    current_limit = number_of_chunks * current_chunk
                    current_out_path = os.path.join(
                        output_path,
                        chunk_file_name % current_chunk
                    )
                    current_out_writer = csv.writer(open(current_out_path, 'w', newline='', encoding=config.csv_encoding))
                    current_out_writer.writerow(headers)
                current_out_writer.writerow(row)


def output_file_name(chunk_file_name: str, chunk: int, output_path='.'):
    return os.path.join(output_path, chunk_file_name % chunk)