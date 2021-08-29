import getopt
import os
import sys
from concurrent.futures import ThreadPoolExecutor


def help():
    print("main.py -i <inputfile> -o <outputfile> -d")
    print("  -i <inputfile> | --input=<inputfile>")
    print("     Define the input file")
    print("  -o <outputfile> | --output=<outputfile>")
    print("     Define the output file")
    print("  -d | --dummy")
    print("     Create dummy file for testing")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:", ["dummy", "input=", "output="])
        if len(opts) == 0:
            help()
            sys.exit(2)
    except getopt.GetoptError:
        help()
        sys.exit(2)

    input_file = ""
    output_file = ""
    should_process = True

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-d", "--dummy"):
            from generator.dummydata import generate_dummy_data
            should_process = False
            generate_dummy_data()

    if should_process:
        if os.path.isfile(output_file):
            os.remove(output_file)

        files = [(input_file, output_file)]
        with ThreadPoolExecutor() as executor:
            from processor.processor import process_file
            executor.map(process_file, files)


if __name__ == "__main__":
    main()
