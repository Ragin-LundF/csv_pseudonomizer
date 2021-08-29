import mmap
from pathlib import Path
from tqdm import tqdm

from processor.row_processor import process_row


def process_file(files):
    input_file = files[0]
    output_file = files[1]
    csv_output = []
    fsize = Path(input_file).stat().st_size
    tot = 0
    print(f"Processing {input_file}")

    with open(input_file, "r+b") as fp:
        # use a progress bar
        with tqdm(total=fsize, desc=input_file) as pbar:
            # map the entire file into memory, normally much faster than buffered i/o
            mm = mmap.mmap(fp.fileno(), 0)
            # iterate over the block, until next newline
            for line in iter(mm.readline, b""):
                csv_output.append(process_row(line.strip()))
                tot += len(line)
                pbar.update(tot - pbar.n)
            mm.close()
    fp.close()

    with open(output_file, "a+") as fp:
        for line in csv_output:
            fp.write(f"{line}")
    fp.close()
