import glob
import mmap
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from faker import Faker
from tqdm import tqdm

import config
from model.parameter_dc import Parameter
from processor.file_split import file_name
from processor.row_processor import process_row
from pseudonomizer.global_dict import init, save_mapping_data
from utils.file_utils import save_list_of_lines


def start_processing(params: Parameter):
    init()
    with ThreadPoolExecutor() as executor:
        executor.map(process_file, [params])


def process_file(params: Parameter):
    fake = Faker(config.fake_locale)
    csv_output = []
    file_size = Path(params.input_file).stat().st_size
    total_processed_in = 0
    print(f"Processing {params.input_file}\n")

    for file in file_name(params):
        with open(file, 'r+b') as fp:
            # use a progress bar
            with tqdm(total=file_size, desc=f"processing {file} (bytes)") as progress_bar_in:
                # map the entire file into memory, normally much faster than buffered i/o
                mm = mmap.mmap(fp.fileno(), 0)
                # iterate over the block, until next newline
                for line in iter(mm.readline, b""):
                    try:
                        processed_output = process_row(fake, line.strip(), len(csv_output) == 0)
                        if processed_output is not None:
                            csv_output.append(processed_output)
                    except ModuleNotFoundError as mnfe:
                        print("The specified module for pseudonomization in the config.py was not found. Error: ", mnfe)
                        break
                    except AttributeError as attrex:
                        print("The specified method for pseudonomization in config.py was not found. Error: ", attrex)
                        break
                    except BaseException as base:
                        print("General error while processing files: ", base)
                        break
                    total_processed_in += len(line)
                    progress_bar_in.update(total_processed_in - progress_bar_in.n)
                mm.close()
        fp.close()

    save_list_of_lines(params.output_file, csv_output, mode='a+')

    if config.save_mapping:
        save_mapping_data()

