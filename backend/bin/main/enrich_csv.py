import re

from os import path, walk, remove

import main.helpers.FileHelper as FileHelper

from main.helpers.Environment import Environment
from main.helpers.Locator import Locator
from main.helpers.NameResolver import NameResolver
from main.helpers.Combiner import Combiner
from main.helpers.CipherSuites import CipherSuites


def loop_through_lines(csv_reader, helpers, output_file):
    for index, packet in enumerate(csv_reader):
        if FileHelper.is_header(index):
            default_header = csv_reader.fieldnames
            helper_headers = [helpers[helper_key].header for helper_key in helpers]
            line = Combiner.combine_fields(default_header + helper_headers, False)

        else:
            joined_default_cells = Combiner.join_default_cells(packet)
            line = Combiner.combine_packet_information(joined_default_cells, helpers, packet)

        FileHelper.write_line(output_file, line)


def print_dicts(helpers):
    for helper_key in helpers:
        helpers[helper_key].print()


def create_helpers():
    return {"locator": Locator(), "name_resolver": NameResolver(), "cipher_suites": CipherSuites()}


def main():
    run(Environment.get_environment())


def run(environment_variables):
    csv_path = environment_variables["csv_path"]
    csv_enriched_path = environment_variables["csv_enriched_path"]

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            helpers = create_helpers()

            if FileHelper.is_normal_csv_file(file):
                new_file = re.sub(".csv$", "-enriched.csv", str(file))
                enrich_file(dirpath, file, helpers, new_file)
                remove(path.join(dirpath, file))

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            if FileHelper.is_enriched_csv_file(file):
                FileHelper.move_file(
                    path.join(dirpath, file),
                    path.join(csv_enriched_path, file)
                )


def enrich_file(dirpath, file, helpers, new_file):
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_reader = FileHelper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, helpers, output_file)

        print_dicts(helpers)


if __name__ == "__main__":
    main()
