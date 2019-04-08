from csv import DictReader
from os import path, remove
from shutil import move
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


def write_download_file(write_row, csv_file, output_file, header):
    write_line(output_file, header)
    csv_reader = get_csv_dict_reader(csv_file)
    for row in csv_reader:
        write_row(output_file, row)


def move_file(old_path, new_path):
    try:
        remove(new_path)
    except OSError:
        pass

    move(old_path, new_path)


def remove_file(file_path):
    remove(file_path)
