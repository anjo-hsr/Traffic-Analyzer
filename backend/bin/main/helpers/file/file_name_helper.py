def is_pcap_file(file):
    file = str(file).lower()
    return file.endswith(".pcap") or file.endswith(".pcapng")


def is_normal_csv_file(file):
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith(".csv") and not file.endswith("-enriched.csv")


def is_enriched_csv_file(file):
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith("-enriched.csv")