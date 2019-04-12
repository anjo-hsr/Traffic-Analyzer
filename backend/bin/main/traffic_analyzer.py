import sys

from os import path

import main.convert_pcap as convert_pcap
import main.enrich_csv as add_information
import main.downloaders.cipher_downloader as get_ciphers
import main.downloaders.mac_vendor_downloader as get_mac


def convert():
    print("Start converting")
    convert_pcap.main()


def download():
    print("Start downloading infos")
    destination_cipher_csv = path.join("..", "files", "cipher_suites.csv")
    get_ciphers.run(destination_cipher_csv)

    destination_mac_csv = path.join("..", "files", "mac_vendor.csv")
    get_mac.run(destination_mac_csv)


def enrich():
    print("Start enriching")
    add_information.main()


def run():
    convert()
    enrich()


def run_all():
    download()
    convert()
    enrich()


def main():
    method = sys.argv[1]

    if method == "convert":
        convert()
    elif method == "download":
        download()
    elif method == "enrich":
        enrich()
    elif method == "run":
        run()
    elif method == "run-all":
        run_all()
    else:
        print(
            "Usage traffic_analyzer.py [option]\n\n"
            "Option:\n"
            "   download:    Download information from IANA and IEEE.\n"
            "   convert:     Converts pcap(ng) files to csv\n"
            "   enrich:      Enriches csvs with additional information\n"
            "   run:         Runs convert and enrich\n"
            "   run-all:     Runs download, convert and enrich"
        )


if __name__ == "__main__":
    main()
