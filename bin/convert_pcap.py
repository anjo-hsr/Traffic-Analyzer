import time

from bin.helpers.Detector import Detector
import bin.helpers.Tshark as TsharkHelper

import os
import platform
import re
import subprocess


def run_thark(filename):
    tshark_x64, tshark_x86 = TsharkHelper.get_windows_defaults()

    new_filename = get_new_filename(filename)

    with open(new_filename, "w") as out_file:
        program_path = None

        if platform.system() == "Windows":
            program_path = test_tshark_windows(tshark_x64, tshark_x86)

        elif platform.system() == "Linux":
            program_path = test_tshark_linux()

        if program_path is None:
            return print_error()

        start_tshark(filename, out_file, program_path)


def test_tshark_windows(tshark_x64, tshark_x86):
    if os.path.isfile(tshark_x86):
        return tshark_x86

    elif os.path.isfile(tshark_x64):
        return tshark_x64

    return None


def test_tshark_linux():
    if os.path.isfile("tshark"):
        return "tshark"

    return None


def start_tshark(filename, out_file, program_path):
    arguments = TsharkHelper.get_arguments(filename)
    subprocess.call([program_path] + arguments, stdout=out_file)


def move_csv(old_path, new_path):
    try:
        os.remove(new_path)
    except OSError:
        pass

    os.rename(old_path, new_path)


def get_new_filename(filename):
    new_filename = re.sub("pcap(ng)?$", "csv", str(filename))
    return new_filename


def print_error():
    print("No wireshark folder found. Please install Wireshark into the standard folder")
    return


def is_pcap_file(file):
    return str(file).endswith(".pcap") or str(file).endswith(".pcapng")


def is_csv_file(file):
    return str(file).endswith(".csv")


def run(environment_variables):
    pcap_path = environment_variables["pcap_path"]
    csv_path = environment_variables["csv_path"]

    for (dirpath, dirnames, filenames) in os.walk(pcap_path):
        for file in filenames:
            if is_pcap_file(file):
                run_thark(os.path.join(dirpath, file))

    for (dirpath, dirnames, filenames) in os.walk(pcap_path):
        for file in filenames:
            if is_csv_file(file):
                move_csv(os.path.join(dirpath, file), os.path.join(csv_path, file))


def main():
    run(Detector.get_environment())


main()
