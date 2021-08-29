import mmap
from pathlib import Path
from tqdm import tqdm

from row_processor import process_row


def process_file(files):
    input_file = files[0]
    output_file = files[1]
    csv_output = []
    fsize = Path(input_file).stat().st_size
    total_processed_in = 0
    total_processed_out = 0
    print(f"Processing {input_file}")

    with open(input_file, "r+b") as fp:
        # use a progress bar
        with tqdm(total=fsize, desc=f"processing {input_file} (bytes)") as progress_bar_in:
            # map the entire file into memory, normally much faster than buffered i/o
            mm = mmap.mmap(fp.fileno(), 0)
            # iterate over the block, until next newline
            for line in iter(mm.readline, b""):
                csv_output.append(process_row(line.strip()))
                total_processed_in += len(line)
                progress_bar_in.update(total_processed_in - progress_bar_in.n)
            mm.close()
    fp.close()

    with open(output_file, "a+") as fp:
        with tqdm(total=len(csv_output), desc=f"writing {output_file} (lines)") as progress_bar_out:
            for line in csv_output:
                total_processed_out += 1
                progress_bar_out.update(total_processed_out - progress_bar_out.n)
                fp.write(f"{line}")
    fp.close()
