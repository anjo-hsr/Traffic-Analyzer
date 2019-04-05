from os import path
from urllib import request


def download_file(url):
    file_name = url.split("/")[-1]
    request.urlretrieve(url, file_name)
    return path.join(".", file_name)
