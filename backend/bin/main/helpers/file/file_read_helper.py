from csv import DictReader


def is_header(line_counter) -> bool:
    return line_counter == 0


def get_csv_dict_reader(csv_file) -> DictReader:
    return DictReader(csv_file, delimiter=',')
