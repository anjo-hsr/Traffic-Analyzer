from csv import DictReader
from os import remove, walk
from shutil import move


def is_header(line_counter):
    return line_counter == 0


def write_line(output_file, line):
    output_file.write(line + "\n")


def get_csv_dict_reader(csv_file):
    return DictReader(csv_file, delimiter=',')


def move_file(old_path, new_path):
    if old_path == new_path:
        return

    try:
        remove_file(new_path)
    except OSError:
        pass

    move(old_path, new_path)


def remove_file(file_path):
    remove(file_path)


def get_file_paths(dir_path, check_method):
    file_paths = []
    for dirpath, _, filenames in walk(dir_path):
        for file in filenames:
            if check_method(file):
                file_paths.append({"path": dirpath, "filename": file})
    return file_paths
