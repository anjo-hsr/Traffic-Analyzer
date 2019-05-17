def write_line(output_file, line) -> None:
    output_file.write(line + "\n")


def write_hash_to_file(hash_path, hash_path_exists, pcap_hash) -> None:
    if not hash_path_exists:
        with open(hash_path, "w") as hash_file:
            write_line(hash_file, pcap_hash)

    with open(hash_path, "a") as hash_file:
        write_line(hash_file, pcap_hash)
