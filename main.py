import getopt
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from processor.file_split import split
from pseudonomizer.global_name_dict import init


def print_help():
    print("main.py -i <inputfile> -o <outputfile> -d")
    print("  -i <inputfile> | --input=<inputfile>")
    print("     Define the input file")
    print("  -o <outputfile> | --output=<outputfile>")
    print("     Define the output file")
    print("  -s | --split=")
    print("     Split CSV file into new files. This option defines the wanted output line amount.")
    print("  -d | --dummy")
    print("     Create dummy file for testing")
    print("  --gen_firstnames")
    print("     Generates a new list of firstnames in the `pseudonominizer/rules/firstnames.txt` file, "
          "depending on the locale in `config.py`.")
    print("  --gen_lastnames")
    print("     Generates a new list of lastnames in the `pseudonominizer/rules/lastnames.txt` file, "
          "depending on the locale in `config.py`.")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:s:", ["dummy", "gen_firstname", "gen_lastname", "input=", "output=", "split="])
        if len(opts) == 0:
            print_help()
            sys.exit(2)
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    input_file = ""
    output_file = ""
    file_split_chunks = 0
    should_process = True

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-s", "--split"):
            file_split_chunks = int(arg)
        elif opt in ("-d", "--dummy"):
            from generator.dummydata import generate_dummy_data
            should_process = False
            generate_dummy_data()
        elif opt in "--gen_firstnames":
            from generator.dummydata import generate_first_names
            generate_first_names()
        elif opt in "--gen_lastnames":
            from generator.dummydata import generate_last_names
            generate_last_names()

    if should_process:
        if os.path.isfile(output_file):
            os.remove(output_file)

        if file_split_chunks == 0:
            init()
            files = [(input_file, output_file)]
            with ThreadPoolExecutor() as executor:
                from processor.processor import process_file
                executor.map(process_file, files)
        else:
            split(input_file, file_split_chunks)


if __name__ == "__main__":
    main()
