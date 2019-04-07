from csv import DictReader
from os import path, remove
from urllib import request


def download_file(url):
    filename = url.split("/")[-1]
    request.urlretrieve(url, filename)
    return path.join(".", filename)


def is_header(line_counter):
    return line_counter == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def get_csv_dict_reader(csv_file):
    return DictReader(csv_file, delimiter=',')


def remove_file(file_path):
    remove(file_path)
