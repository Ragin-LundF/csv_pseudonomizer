# CSV File pseudonomizer

This tool replaces data in big CSV files with pseudo data.

## Structure

- `generator` - contains the code for the dummy data generator
- `processor` - main processing logic
- `pseudonomizer` - methods to pseudonomize the data

## Configuration

To configure the tool, please have a look at [config.py](config.py).

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
| `-o` | Specify the output file for processing | `-o dummy_processed.csv` |
| `--outputfile=` | | `--outputfile=dummy_processed.csv` |

### Create a dummy file for testing

```bash
python main.py -d
```

### Split a file into chunks

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

