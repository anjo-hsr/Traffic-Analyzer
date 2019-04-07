import sys

import main.convert_pcap as convert_pcap
import main.enrich_csv as add_information


def convert():
    print("Start converting")
    convert_pcap.main()


def enrich():
    print("Start enriching")
    add_information.main()


def run():
    convert()
    enrich()


def main():
    method = sys.argv[1]
    print(method)
    if method == "convert":
        convert()
    elif method == "enrich":
        enrich()
    elif method == "run":
        run()
    else:
        print("Please use (convert|enrich|run)")


if __name__ == "__main__":
    main()
