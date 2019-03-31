from bin.helpers.Locator import Locator
from bin.helpers.NameResolver import NameResolver
from bin.helpers.Timer import Timer
from bin.helpers.Combiner import Combiner

import csv
import re
import platform
from os import path, walk


def is_header(line_number):
    return line_number == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def loop_through_lines(csv_delimiter, csv_reader, locator, name_resolver, output_file):
    timers = {"fqdn": Timer(), "location": Timer(), "file_writer": Timer()}
    for index, packet in enumerate(csv_reader):
        joined_default_cells = Combiner.join_default_cells(packet, csv_delimiter)
        if is_header(index):
            line = Combiner.combine_header(joined_default_cells, locator, name_resolver)

        else:
            line = Combiner.combine_packet_information(joined_default_cells, locator, name_resolver, packet, timers)

        timers["file_writer"].start_lap()
        write_line(output_file, line)
        timers["file_writer"].end_lap()

    print(timers["fqdn"].print_time_sum())
    print(timers["location"].print_time_sum())
    print(timers["file_writer"].print_time_sum())


def print_dicts(dicts):
    for dict_element in dicts:
        dict_element.print_fqdns()


def main():
    csv_path = path.join(".", "files")

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            if is_csv_file(file):
                new_file = re.sub(".csv$", "-enriched.csv", str(file))

                locator = Locator()
                name_resolver = NameResolver()
                with \
                        open(dirpath + file, mode="r", encoding='utf-8') as capture, \
                        open(dirpath + new_file, 'w', encoding='utf-8') as output_file:
                    csv_delimiter = ","
                    csv_reader = csv.DictReader(capture, delimiter=csv_delimiter)

                    loop_through_lines(csv_delimiter, csv_reader, locator, name_resolver, output_file)

                    print_dicts([locator, name_resolver])


def is_csv_file(file):
    return str(file).endswith(".csv")


timer = Timer()
main()
timer.set_end_time()
timer.print_runtime()
