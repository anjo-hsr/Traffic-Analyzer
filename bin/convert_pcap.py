from os import path, walk
import re
import platform
import shlex
import subprocess


def run_thark_windows(filename):
    x86_path = "C:\\Program Files (x86)\\Wireshark\\"
    x64_path = "C:\\Program Files\\Wireshark\\"
    program = "tshark"

    file_argumnets = ["-r", filename]
    export_arguments = " -T fields" \
                       " -e frame.time -e frame.cap_len" \
                       " -e eth.dst -e eth.src" \
                       " -e ip.dst -e ip.src -e ip.proto" \
                       " -e tcp.srcport -e tcp.dstport -e tcp.flags" \
                       " -e udp.srcport -e udp.srcport" \
                       " -E header=y -E separator=, -E quote=d -E occurrence=f"

    arguments = shlex.split(export_arguments)

    combined_args = file_argumnets + arguments

    new_filename = re.sub("pcap(ng)?$", "csv", str(filename))

    with open(new_filename, "w") as out_file:
        if path.isdir(x86_path):
            subprocess.Popen([x86_path + program] + combined_args, stdout=out_file)

        elif path.isdir(x64_path):
            subprocess.Popen([x64_path + program] + combined_args, stdout=out_file)

        else:
            print("No wireshark folder found. Please install Wireshark into the defined standard folder")


def run_thark_unix():
    pass


def main():
    os_vendor = platform.system()

    directory_character = {
        "Windows": "\\",
        "Unix": "/"
    }

    pcap_path = "..{0}docker{0}pcaps".format(directory_character[os_vendor])
    for (dirpath, dirnames, filenames) in walk(pcap_path):
        for file in filenames:
            if str(file).endswith(".pcap") or str(file).endswith(".pcapng"):
                run_thark_windows(dirpath + directory_character[os_vendor] + file)


main()
