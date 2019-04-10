import platform
import re
import subprocess

from os import path, walk

import main.helpers.FileHelper as FileHelper
import main.helpers.Tshark as TsharkHelper

from main.helpers.Environment import Environment


def run_tshark(filename):
    new_filename = get_new_filename(filename)

    with open(new_filename, "w") as out_file:
        program_path = detect_platform()

        if program_path is None:
            return print_error()

        start_tshark(filename, out_file, program_path)


def detect_platform():
    program_path = None

    if platform.system() == "Windows":
        program_path = test_tshark_windows()

    elif platform.system() == "Linux":
        program_path = test_tshark_linux()

    return program_path


def test_tshark_windows():
    windows_defaults = TsharkHelper.get_windows_defaults()

    if path.isfile(windows_defaults["x86"]):
        return windows_defaults["x86"]

    elif path.isfile(windows_defaults["x64"]):
        return windows_defaults["x64"]

    return None


def test_tshark_linux():
    if path.isfile("/usr/bin/tshark"):
        return "tshark"

    return None


def start_tshark(filename, out_file, program_path):
    arguments = TsharkHelper.get_arguments(filename)
    subprocess.run([program_path] + arguments, stdout=out_file)


def get_new_filename(filename):
    new_filename = re.sub("^(.*[/\\\\])?(capture-)?(.*)pcap(ng)?$", "\g<1>capture-\g<3>csv", str(filename).lower())
    return new_filename


def print_error():
    print("No wireshark folder found. Please install Wireshark into the standard folder")
    return


def main():
    run(Environment.get_environment())


def run(environment_variables):
    pcap_path = environment_variables["pcap_path"]
    csv_path = environment_variables["csv_path"]

    for (dirpath, dirnames, filenames) in walk(pcap_path):
        for file in filenames:
            if FileHelper.is_pcap_file(file):
                run_tshark(path.join(dirpath, file))

    for (dirpath, dirnames, filenames) in walk(pcap_path):
        for file in filenames:
            if FileHelper.is_normal_csv_file(file):
                FileHelper.move_file(
                    path.join(dirpath, file),
                    path.join(csv_path, file)
                )


if __name__ == "__main__":
    main()
