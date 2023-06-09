import argparse

from reader import InputReader
from generator import Generator

def main():
    # Defining and parsing the command line flags
    parser = argparse.ArgumentParser(
        description='Generate realistic mock data based on complex user inputs.',
    )

    parser.add_argument('-i', '--input', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', help='(optional) Path to the output folder. If not specified will print to stdout')
    args = parser.parse_args()

    input_reader = InputReader(args.input, args.output)
    generatorSettings = input_reader.read_input()
    generator = Generator(generatorSettings)
    if "output" in parser.parse_args():
        generator.generate(input_reader.output_file)
    else:
        generator.generate()