import sys

import main.convert_pcap as convert_pcap
import main.add_information as add_information


def convert():
    convert_pcap.main()


def enrich():
    add_information.main()


def run():
    convert()
    enrich()

switcher = {
    "convert": convert(),
    "enrich": enrich(),
    "run": run()
}

if __name__ == "__main__":
    switcher.get(sys.argv[0])
