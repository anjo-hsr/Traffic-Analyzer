import subprocess
from os import path

import main.helpers.tshark_helper as tshark_helper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_name_helper, file_path_helper, file_read_helper, file_write_helper
from main.helpers.file.file_name_helper import get_new_filename
from main.helpers.platform_detection_helper import PlatformDetectionHelper
from main.helpers.print_helper import PrintHelper


def run_tshark(filename, pcap_file_path, csv_file_path) -> None:
    program_path = PlatformDetectionHelper.detect_tshark()
    if program_path is None:
        error_text = "No wireshark folder found. Please install Wireshark into the standard folder"
        PrintHelper.print_error(error_text)
        return

    csv_filename = get_new_filename(filename, "csv", "capture-")

    full_pcap_filename = path.join(pcap_file_path, filename)
    full_csv_filename = path.join(csv_file_path, csv_filename)
    with open(full_csv_filename, "w") as csv_file:
        start_tshark(full_pcap_filename, csv_file, program_path)
        return


def start_tshark(pcap_file, csv_file, program_path) -> None:
    arguments = tshark_helper.get_arguments(pcap_file)
    subprocess.run([program_path] + arguments, stdout=csv_file)


def main() -> None:
    environment_helper = EnvironmentHelper()
    run(environment_helper.get_environment())


def run(environment_variables) -> None:
    config_name = "traffic-analyzer.conf"
    key = "pcap_location"
    pcap_path = file_read_helper.get_config_value(config_name, key)

    csv_tmp_path = environment_variables["csv_tmp_path"]
    hash_path = path.join(csv_tmp_path, "hashes.txt")
    file_hashes = file_read_helper.get_file_hashes(hash_path)

    for file_path in file_path_helper.get_file_paths(pcap_path, file_name_helper.is_pcap_file):
        pcap_hash = file_read_helper.get_file_hashsum(path.join(file_path["path"], file_path["filename"]))
        if pcap_hash in file_hashes:
            continue

        run_tshark(file_path["filename"], file_path["path"], csv_tmp_path)
        file_write_helper.write_hash_to_file(hash_path, pcap_hash)


if __name__ == "__main__":
    main()
