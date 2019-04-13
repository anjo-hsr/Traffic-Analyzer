from os import path
from urllib import request

from main.helpers import file_helper
from main.helpers.environment_helper import EnvironmentHelper


class DownloadHelper:

    @staticmethod
    def download_file(destination_file, url, header, write_row):
        filename = DownloadHelper.store_file(url)

        with \
                open(filename, mode="r", encoding='utf-8') as csv_file, \
                open(destination_file, mode='w', encoding='utf-8') as output_file:
            DownloadHelper.write_download_file(write_row, csv_file, output_file, header)

        return filename

    @staticmethod
    def store_file(url):
        environment_helper = EnvironmentHelper()
        environment_variables = environment_helper.get_environment()

        url_filename = url.split("/")[-1]
        filename = path.join(environment_variables["csv_tmp_path"], url_filename)
        request.urlretrieve(url, filename)
        return path.join(".", filename)

    @staticmethod
    def write_download_file(write_row, csv_file, output_file, header):
        file_helper.write_line(output_file, header)
        csv_reader = file_helper.get_csv_dict_reader(csv_file)
        for row in csv_reader:
            write_row(output_file, row)
