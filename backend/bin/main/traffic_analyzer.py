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
    else:
        print("Please use (convert|enrich|run)")


if __name__ == "__main__":
    main()
