import mmap
from pathlib import Path

from faker import Faker
from tqdm import tqdm

import config
from processor.row_processor import process_row
from pseudonomizer.global_dict import save_dataframe, load_dataframe


def process_file(files: list[str]):
    fake = Faker(config.fake_locale)
    input_file = files[0]
    output_file = files[1]
    csv_output = []
    file_size = Path(input_file).stat().st_size
    total_processed_in = 0
    print(f"Processing {input_file}")

    if config.save_mapping:
        load_dataframe()

    with open(input_file, 'r+b', encoding=config.csv_encoding) as fp:
        # use a progress bar
        with tqdm(total=file_size, desc=f"processing {input_file} (bytes)") as progress_bar_in:
            # map the entire file into memory, normally much faster than buffered i/o
            mm = mmap.mmap(fp.fileno(), 0)
            # iterate over the block, until next newline
            for line in iter(mm.readline, b""):
                csv_output.append(process_row(fake, line.strip()))
                total_processed_in += len(line)
                progress_bar_in.update(total_processed_in - progress_bar_in.n)
            mm.close()
    fp.close()

    save_result(output_file, csv_output)

    if config.save_mapping:
        save_dataframe()


def save_result(output_file: str, csv_output: list[str]):
    total_processed_out = 0
    with open(output_file, 'a+', encoding=config.csv_encoding, newline='') as fp:
        with tqdm(total=len(csv_output), desc=f"writing {output_file} (lines)") as progress_bar_out:
            for line in csv_output:
                total_processed_out += 1
                progress_bar_out.update(total_processed_out - progress_bar_out.n)
                fp.write(f"{line}\n")
    fp.close()
