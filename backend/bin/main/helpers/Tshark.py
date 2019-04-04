import shlex

from os import path, environ


def get_windows_defaults():
    system_drive = environ['SYSTEMDRIVE']

    # environ["ProgramFiles"] could be used to simplify the variables but there is no guaranty
    # that Wireshark x64 is installed on a x64 Windows
    windows_defaults = {
        "x86": path.join(system_drive, "Program Files (x86)", "Wireshark", "tshark.exe"),
        "x64": path.join(system_drive, "Program Files", "Wireshark", "tshark.exe")
    }
    return windows_defaults


def get_arguments(filename):
    file_argumnets = ["-r", filename]
    export_arguments = " -T fields" \
                       " -e frame.time -e frame.cap_len" \
                       " -e eth.dst -e eth.src" \
                       " -e ip.dst -e ip.src -e ip.proto" \
                       " -e tcp.srcport -e tcp.dstport -e tcp.flags -e tcp.len -e tcp.stream" \
                       " -e udp.srcport -e udp.dstport -e udp.length" \
                       " -e http.request.method -e http.request.uri" \
                       " -e tls.record.version -e tls.handshake.ciphersuite -e tls.handshake.ciphersuites" \
                       " -E header=y -E separator=, -E quote=d -E occurrence=f"

    arguments = shlex.split(export_arguments)
    combined_args = file_argumnets + arguments
    return combined_args
