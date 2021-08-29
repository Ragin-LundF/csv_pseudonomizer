import getopt
import sys
from concurrent.futures import ThreadPoolExecutor


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:", ["dummy", "input=", "output="])
    except getopt.GetoptError:
        print("main.py -i <inputfile> -o <outputfile> -d <true|false>")
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
        files = [(input_file, output_file)]
        with ThreadPoolExecutor() as executor:
            from processor.processor import process_file
            executor.map(process_file, files)


if __name__ == "__main__":
    main()
