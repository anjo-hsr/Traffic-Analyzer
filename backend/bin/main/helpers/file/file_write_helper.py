from os import path


def write_line(output_file, line) -> None:
    output_file.write(line + "\n")


def write_lines(output_file, lines) -> None:
    for line in lines:
        write_line(output_file, line)


def write_hash_to_file(hash_path, pcap_hash) -> None:
    if not path.isfile(hash_path):
        with open(hash_path, "w") as hash_file:
            write_line(hash_file, pcap_hash)

    with open(hash_path, "a") as hash_file:
        write_line(hash_file, pcap_hash)
