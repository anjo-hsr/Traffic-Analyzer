import re


def is_pcap_file(file) -> bool:
    file = str(file).lower()
    return file.endswith(".pcap") or file.endswith(".pcapng")


def is_normal_csv_file(file) -> bool:
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith(".csv") and not file.endswith("-enriched.csv")


def is_enriched_csv_file(file) -> bool:
    file = str(file).lower()
    return file.startswith("capture-") and file.endswith("-enriched.csv")


def get_new_filename(filename, new_extension, prefix="", suffix="") -> str:
    new_filename = re.sub(
        r"^(.*[/\\])?(" + prefix + r")?(.*)(" + suffix + r")?\.(.*)$",
        r"\g<1>" + prefix + r"\g<3>" + suffix + r"." + new_extension,
        str(filename).lower())
    return new_filename
