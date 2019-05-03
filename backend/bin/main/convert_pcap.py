import platform
import re
import subprocess
from os import path

import main.helpers.file.file_helper as file_helper
import main.helpers.tshark_helper as tshark_helper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.print_helper import PrintHelper


def run_tshark(filename):
    new_filename = get_new_filename(filename)

    with open(new_filename, "w") as out_file:
        program_path = detect_platform()
        if program_path is None:
            error_text = "No wireshark folder found. Please install Wireshark into the standard folder"
            return PrintHelper.print_error(error_text)

        start_tshark(filename, out_file, program_path)

    return None


def detect_platform():
    program_path = None

    if platform.system() == "Windows":
        program_path = test_tshark_windows()

    elif platform.system() == "Linux":
        program_path = test_tshark_linux()

    return program_path


def test_tshark_windows():
    windows_defaults = tshark_helper.get_windows_defaults()
    return_value = None

    if path.isfile(windows_defaults["x86"]):
        return_value = windows_defaults["x86"]

    elif path.isfile(windows_defaults["x64"]):
        return_value = windows_defaults["x64"]

    return return_value


def test_tshark_linux():
    if path.isfile("/usr/bin/tshark"):
        return "tshark"

    return None


def start_tshark(filename, out_file, program_path):
    arguments = tshark_helper.get_arguments(filename)
    subprocess.run([program_path] + arguments, stdout=out_file)


def get_new_filename(filename):
    new_filename = re.sub(
        r"^(.*[/\\])?(capture-)?(.*)pcap(ng)?$",
        r"\g<1>capture-\g<3>csv",
        str(filename).lower())
    return new_filename


def main():
    environment_helper = EnvironmentHelper()
    run(environment_helper.get_environment())


def run(environment_variables):
    pcap_path = environment_variables["pcap_path"]
    pcap_processed_path = environment_variables["pcap_processed_path"]
    csv_tmp_path = environment_variables["csv_tmp_path"]

    for file_path in file_helper.get_file_paths(pcap_path, file_helper.is_pcap_file):
        run_tshark(path.join(file_path["path"], file_path["filename"]))
        file_helper.move_file(
            path.join(file_path["path"], file_path["filename"]),
            path.join(pcap_processed_path, file_path["filename"])
        )

    for file_path in file_helper.get_file_paths(pcap_path, file_helper.is_normal_csv_file):
        file_helper.move_file(
            path.join(file_path["path"], file_path["filename"]),
            path.join(csv_tmp_path, file_path["filename"])
        )


if __name__ == "__main__":
    main()
