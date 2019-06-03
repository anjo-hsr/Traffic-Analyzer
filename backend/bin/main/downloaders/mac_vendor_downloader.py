import re
from os import path

from main.combiners.field_combiner import FieldCombiner
from main.helpers.download_helper import DownloadHelper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_move_helper, file_write_helper
from main.helpers.string_helper import enclose_with_quotes


def convert_mac_address(row) -> str:
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def write_row(output_file, row) -> None:
    mac_address = convert_mac_address(row)
    line = mac_address + FieldCombiner.delimiter + enclose_with_quotes(row["Organization Name"])
    file_write_helper.write_line(output_file, line)


def main() -> None:
    environment_helper = EnvironmentHelper()
    environment_variables = environment_helper.get_environment()
    destination_mac_csv = path.join(environment_variables["csv_list_path"], "mac_vendor.csv")
    run(destination_mac_csv)


def run(destination_file) -> None:
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    header = "eth_short,vendor"
    filename = DownloadHelper.download_file(destination_file, url, header, write_row)
    file_move_helper.remove_file(filename)


if __name__ == "__main__":
    main()
