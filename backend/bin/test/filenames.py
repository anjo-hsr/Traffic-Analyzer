from typing import List, Dict


def get_filenames() -> Dict[str, List[str]]:
    return {
        "csv_filenames": ["capture-test_lower.csv", "capture-test_double_ending.py.csv",
                          "capture-test_upper.CSV", "capture-test_camel.Csv"],

        "csv_enriched_filenames": ["capture-test_lower-enriched.csv", "capture-test_double_ending.py-enriched.csv",
                                   "capture-test_upper-enriched.CSV", "capture-test_camel-enriched.Csv"],

        "pcap_filenames_without_prefix": ["test_lower.pcap", "capture-test_double_ending.py.pcap",
                                          "capture-test_upper.PCAP", "capture-test_camel.Pcap"],

        "pcapng_filenames_without_prefix": ["test_lower.pcapng", "capture-test_double_ending.py.pcapng",
                                            "capture-test_upper.PCAPNG", "capture-test_camel.Pcapng"],

        "pcap_filenames_with_prefix": ["capture-test_lower.pcap", "capture-test_double_ending.py.pcap",
                                       "capture-test_upper.PCAP", "capture-test_camel.Pcap"],

        "pcapng_filenames_with_prefix": ["capture-test_lower.pcapng", "capture-test_double_ending.py.pcapng",
                                         "capture-test_upper.PCAPNG", "capture-test_camel.Pcapng"]
    }
