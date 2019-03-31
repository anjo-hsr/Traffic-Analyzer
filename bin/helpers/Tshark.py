import shlex


def get_windows_defaults():
    x86_path = "C:\\Program Files (x86)\\Wireshark\\"
    x64_path = "C:\\Program Files\\Wireshark\\"
    program = "tshark.exe"
    tshark_x86 = x86_path + program
    tshark_x64 = x64_path + program
    return tshark_x64, tshark_x86


def get_arguments(filename):
    file_argumnets = ["-r", filename]
    export_arguments = " -T fields" \
                       " -e frame.time -e frame.cap_len" \
                       " -e eth.dst -e eth.src" \
                       " -e ip.dst -e ip.src -e ip.proto" \
                       " -e tcp.srcport -e tcp.dstport -e tcp.flags -e tcp.payload" \
                       " -e udp.srcport -e udp.srcport" \
                       " -E header=y -E separator=, -E quote=d -E occurrence=f"
    arguments = shlex.split(export_arguments)
    combined_args = file_argumnets + arguments
    return combined_args
