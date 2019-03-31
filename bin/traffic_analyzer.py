import bin.add_information as add_information
import bin.convert_pcap as convert_pcap

from bin.helpers.Environment import Environment


def main():
    convert_pcap.run(Environment.get_environment())

    # Current bug: Not waiting for tshark to be finished.
    # add_information.main()
