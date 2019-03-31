import bin.add_information as add_information
import bin.convert_pcap as convert_pcap


def main():
    convert_pcap.main()

    # Current bug: Not waiting for tshark to be finished.
    # add_information.main()