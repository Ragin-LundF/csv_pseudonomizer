import getopt
import os
import sys

from model.parameter_dc import Parameter
from processors.file_split import split


def print_help():
    print('main.py -i <inputfile> -o <outputfile> -d')
    print('  -i <inputfile> | --input=<inputfile>')
    print('     Define the input file')
    print('  -o <outputfile> | --output=<outputfile>')
    print('     Define the output file')
    print('  -s | --split=')
    print('     Split CSV file into new files. This option defines the wanted output line amount.')
    print('  -d | --dummy')
    print('     Create dummy file for testing')
    print('  -a')
    print('     Read split files and append results to one big file')
    print('  --gen_firstnames')
    print('     Generates a new list of firstnames in the `pseudonominizer/rules/firstnames.txt` file, '
          'depending on the locale in `config.py`.')
    print('  --gen_lastnames')
    print('     Generates a new list of lastnames in the `pseudonominizer/rules/lastnames.txt` file, '
          'depending on the locale in `config.py`.')


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dai:o:s:',
                                   ['dummy', 'gen_firstname', 'gen_lastname', 'input=', 'output=', 'split='])
        if len(opts) == 0:
            print_help()
            sys.exit(2)
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    parameter = Parameter(None, None)
    parameter.input_file = ''
    parameter.output_file = ''
    file_split_chunks = 0
    should_process = True

    for opt, arg in opts:
        if opt in ('-i', '--input'):
            parameter.input_file = arg
        elif opt in ('-o', '--output'):
            parameter.output_file = arg
        elif opt in ('-s', '--split'):
            file_split_chunks = int(arg)
        elif opt in '-a':
            parameter.is_split_file = True
        elif opt in ('-d', '--dummy'):
            from generator.dummydata import generate_dummy_data
            should_process = False
            generate_dummy_data()
        elif opt in '--gen_firstnames':
            from generator.dummydata import generate_first_names
            generate_first_names()
        elif opt in '--gen_lastnames':
            from generator.dummydata import generate_last_names
            generate_last_names()

    if should_process:
        if os.path.isfile(parameter.output_file):
            os.remove(parameter.output_file)

        if file_split_chunks == 0:
            from processors.processor import start_processing
            start_processing(parameter)
        else:
            split(parameter.input_file, file_split_chunks)


if __name__ == '__main__':
    main()
