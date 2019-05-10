from csv import DictReader


def is_header(line_counter):
    return line_counter == 0


def get_csv_dict_reader(csv_file):
    return DictReader(csv_file, delimiter=',')


def get_config_value(file_path, key):
    key_index = 0
    value_index = 1
    value = ""

    with open(file_path) as config_file:
        for line in config_file:
            key_value = line.replace(" ", "").split("=")
            if key_value[key_index] == key:
                value = key_value[value_index]
                break

    return value
