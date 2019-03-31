import bin.add_information as add_information
import bin.convert_pcap as convert_pcap

from bin.helpers.Detector import Detector


def main():
    convert_pcap.run(Detector.get_environment())

    # Current bug: Not waiting for tshark to be finished.
    # add_information.main()
