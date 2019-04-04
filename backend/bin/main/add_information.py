import csv
import re

from os import path, walk


from main.helpers.Environment import Environment
from main.helpers.Locator import Locator
from main.helpers.NameResolver import NameResolver
from main.helpers.Combiner import Combiner
from main.helpers.CipherSuites import CipherSuites


def is_header(line_number):
    return line_number == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def loop_through_lines(csv_delimiter, csv_reader, helpers, output_file):
    for index, packet in enumerate(csv_reader):
        if is_header(index):
            default_header = csv_reader.fieldnames
            helper_headers = [helpers[helper_key].header for helper_key in helpers]
            line = Combiner.combine_fields(default_header + helper_headers, False)

        else:
            joined_default_cells = Combiner.join_default_cells(packet, csv_delimiter)
            line = Combiner.combine_packet_information(joined_default_cells, helpers, packet)

        write_line(output_file, line)


def print_dicts(helpers):
    for helper_key in helpers:
        helpers[helper_key].print()


def main():
    run(Environment.get_environment())


def run(environment_variables):
    csv_path = environment_variables["csv_path"]

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            helpers = create_helpers()

            if is_normal_csv_file(file):
                new_file = re.sub(".csv$", "-enriched.csv", str(file))
                enrich_file(dirpath, file, helpers, new_file)


def is_normal_csv_file(file):
    file = str(file).lower()
    return file.startswith("capture") and file.endswith(".csv") and not file.endswith("-enriched.csv")


def create_helpers():
    return {"locator": Locator(), "name_resolver": NameResolver(), "cipher_suites": CipherSuites()}


def enrich_file(dirpath, file, helpers, new_file):
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_delimiter = ","
        csv_reader = csv.DictReader(capture, delimiter=csv_delimiter)

        loop_through_lines(csv_delimiter, csv_reader, helpers, output_file)

        print_dicts(helpers)


main()
