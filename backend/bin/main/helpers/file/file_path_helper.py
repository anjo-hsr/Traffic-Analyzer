from os import walk
from typing import List, Dict


def get_file_paths(dir_path, check_method) -> List[Dict[str, str]]:
    file_paths = []
    for dirpath, _, filenames in walk(dir_path):
        for file in filenames:
            if check_method(file):
                file_paths.append({"path": dirpath, "filename": file})
    return file_paths
