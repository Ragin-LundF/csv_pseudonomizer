# CSV File pseudonomizer

This tool replaces data in big CSV files with pseudo data.

## Structure

- `generator` - contains the code for the dummy data generator
- `model` - data classes
- `processors` - main processing logic
- `pseudonomizer` - methods to pseudonomize the data
- `utils` - util methods


## Installation

### Prerequisites
#### Cent OS
- GCC
- Python 3.9
- Pip

#### Windows
- Visual C++ Library (https://visualstudio.microsoft.com/de/visual-cpp-build-tools/)
- Python 3.9
- Pip

### Application checkout and preparation
```git
git clone https://github.com/Ragin-LundF/csv_pseudonomizer.git
cd csv_pseudonomizer
pip install -r requirements.txt
```


## Configuration

### General configuration
To configure the tool, please have a look at [config.py](config.py).

### Names list
To replace names in the CSV, the tool requires lists of names which should be replaced.
- [firstnames.txt](pseudonomizer/rules/firstnames.txt)
- [lastnames.txt](pseudonomizer/rules/lastnames.txt)

### Company Regexes
To keep company names, you can add regex to find a company.
This is because companies are not under GDPR.
The regexes can be found under:
- [company_regexes.py](pseudonomizer/rules/company_regexes.py)

## Usage

| Parameter | Description | Example |
| --- | --- | --- |
| none | Print out help | n/a |
| `-d` | Create a dummy file for testing (see `config.py` for file names) | `-d` |
| `--dummy` | | `--dummy` |
| `-i` | Specify the input file for processing | `-i dummy.csv` |
| `--inputfile=` | | `--inputfile=dummy.csv` |
| `-s` | Split CSV file into new files. This option defines the wanted output line amount. | `-s 5000` |
| `--split=` | | `--split=5000` |
| `-a` | Append split files to one output file. It detects the files, which are split by the `-s` parameter. It is required to set input and output file. See examples for split file processing for more information.| `-a` |
| `-o` | Specify the output file for processing | `-o dummy_processed.csv` |
| `--outputfile=` | | `--outputfile=dummy_processed.csv` |
| `--gen_firstnames` | Generates a new list of firstnames in the `pseudonominizer/rules/firstnames.txt` file, depending on the locale in `config.py`. | `--gen_firstnames` |
| `--gen_lastnames` | Generates a new list of lastnames in the `pseudonominizer/rules/lastnames.txt` file, depending on the locale in `config.py`. | `--gen_lastnames` |

### Create a dummy file for testing

```bash
python main.py -d
```

### Split a file into chunks

#### Splitting
Short:
```bash
python main.py -i <inputfile> -s <lines for new files>
```

Long:
```bash
python main.py --inputfile=<inputfile> --split=<lines for new files>
```

Example:
```bash
python main.py -i dummy.csv -s 5000
```


### Process a file

Short:
```bash
python main.py -i <inputfile> -o <outputfile>
```

Long:
```bash
python main.py --inputfile=<inputfile> --outputfile=<outputfile>
```

Example:
```bash
python main.py -i=dummy.csv -o=dummy_processed.csv
```

### Process a set of split files

Short:
```bash
python main.py -i <inputfile> -o <outputfile> -a
```

Long:
```bash
python main.py --inputfile=<inputfile> --outputfile=<outputfile> -a
```

Example:
```bash
python main.py -i=dummy.csv -o=dummy_processed.csv -a
```
This will detect all `dummy_chunk_*.csv` files and process them into one big output file.
The `-i` parameter is used here to define the main file name.
`-a` takes the config `split_file_template_trailing` and replaces the `%s` with an asterisk to find all the related files.

If you have multiple files which are not split with this tool, please name them as:
`<filename>_chunk_<number>.csv`.

Example:
- `dummy_chunk_0001.csv`
- `dummy_chunk_0002.csv`
- `dummy_chunk_0003.csv`

### Generate new name lists

Firstnames:
```bash
python main.py --gen-firstnames
```

Lastnames:
```bash
python main.py --gen-lastnames
```

# Performance

## Create Dummy Data
Create dummy data is a functionality to create test samples.
It uses the defined cores in the configuration and pushes all data first into the RAM.
This process requires big machines with a large amount of RAM if you want to create really big data.

To create 50.000.000 records a minimum of 50 GB RAM is recommended.
A regular notebook with 32 GB RAM can create 1.000.000 records in ~7 minutes (tested on AMD Ryzen 4700X).

The processing of the data is a bit faster.
In the default configuration (as-it-is) the tool can process on an AMD Ryzen 4700X with 32 GB RAM:
- 1.000.000 records in ~2,5 minutes
- 10.000.000 records in ~27 minutes.

The performance is more or less linear, which means, if you want to process 100.000.000 records, you need ~270 minutes.

If new rules should be used, try to avoid regular expressions, because they are extremely slow.
Each rule decreases also the performance.
