from os import remove
from shutil import move


def move_file(old_path, new_path) -> None:
    if old_path == new_path:
        return

    try:
        remove_file(new_path)
    except OSError:
        pass

    move(old_path, new_path)


def remove_file(file_path) -> None:
    remove(file_path)
