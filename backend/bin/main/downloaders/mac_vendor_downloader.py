import re
from os import path
from typing import Dict, TextIO

from main.helpers.download_helper import DownloadHelper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_move_helper, file_write_helper
from main.helpers.string_helper import get_mac_address_line


def convert_mac_address(row: Dict[str, str]) -> str:
    vendor_part = row["Assignment"].lower()
    mac_address_array = re.findall("..?", vendor_part)
    return ":".join(mac_address_array)


def get_local_mac_address(universal_mac_address: str) -> str:
    mac_int_value = int(universal_mac_address.replace(":", ""), 16)

    local_identifier = 0x020000
    local_mac_int_value = mac_int_value | local_identifier
    local_mac_hex_value = format(local_mac_int_value, "06x")

    mac_address_array = re.findall("..?", local_mac_hex_value.replace("0x", ""))
    return ":".join(mac_address_array)


def write_row(output_file: TextIO, row: Dict[str, str]) -> None:
    universal_mac_address = convert_mac_address(row)
    universal_line = get_mac_address_line(universal_mac_address, row["Organization Name"], False)

    local_mac_address = get_local_mac_address(universal_mac_address)
    local_line = get_mac_address_line(local_mac_address, row["Organization Name"], True)

    file_write_helper.write_lines(output_file, [universal_line, local_line])


def main() -> None:
    environment_helper = EnvironmentHelper()
    environment_variables = environment_helper.get_environment()
    destination_mac_csv = path.join(environment_variables["csv_list_path"], "mac_vendor.csv")
    run(destination_mac_csv)


def run(destination_file: str) -> None:
    # Yes IEEE uses still simple, unencrypted http...
    url = "http://standards-oui.ieee.org/oui/oui.csv"
    header = "eth_short,vendor"
    filename = DownloadHelper.download_file(destination_file, url, header, write_row)
    file_move_helper.remove_file(filename)


if __name__ == "__main__":
    main()
