from csv import DictReader
from os import path, remove
from shutil import move
from urllib import request

from main.helpers.environment_helper import EnvironmentHelper


def download_file(url):
    environment_helper = EnvironmentHelper()

    url_filename = url.split("/")[-1]
    environment_variables = environment_helper.get_environment()

    filename = path.join(environment_variables["csv_tmp_path"], url_filename)
    request.urlretrieve(url, filename)
    return path.join(".", filename)


def is_header(line_counter):
    return line_counter == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def get_csv_dict_reader(csv_file):
    return DictReader(csv_file, delimiter=',')


def write_download_file(write_row, csv_file, output_file, header):
    write_line(output_file, header)
    csv_reader = get_csv_dict_reader(csv_file)
    for row in csv_reader:
        write_row(output_file, row)


def move_file(old_path, new_path):
    if old_path == new_path:
        return

    try:
        remove(new_path)
    except OSError:
        pass

    move(old_path, new_path)


def remove_file(file_path):
    remove(file_path)


def is_pcap_file(file):
    return str(file).lower().endswith(".pcap") or str(file).lower().endswith(".pcapng")


def is_normal_csv_file(file):
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith(".csv") and not file.endswith("-enriched.csv")


def is_enriched_csv_file(file):
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith(".csv") and file.endswith("-enriched.csv")
