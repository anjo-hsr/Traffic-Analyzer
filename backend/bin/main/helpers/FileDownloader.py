from os import path
from urllib import request


def download_file(url):
    filename = url.split("/")[-1]
    request.urlretrieve(url, filename)
    return path.join(".", filename)
