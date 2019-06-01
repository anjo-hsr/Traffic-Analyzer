from typing import List, Dict


def get_filenames() -> Dict[str, List[str]]:
    return {
        "csv_filenames": ["prefix-test_lower.csv", "prefix-test_double_ending.py.csv",
                          "prefix-test_upper.CSV", "prefix-test_camel.Csv"],

        "csv_enriched_filenames": ["prefix-test_lower-suffix.csv", "prefix-test_double_ending.py-suffix.csv",
                                   "prefix-test_upper-suffix.CSV", "prefix-test_camel-suffix.Csv"],

        "pcap_filenames_without_prefix": ["test_lower.pcap", "test_double_ending.py.pcap",
                                          "test_upper.PCAP", "test_camel.Pcap"],

        "pcapng_filenames_without_prefix": ["test_lower.pcapng", "test_double_ending.py.pcapng",
                                            "test_upper.PCAPNG", "test_camel.Pcapng"],

        "pcap_filenames_with_prefix": ["prefix-test_lower.pcap", "prefix-test_double_ending.py.pcap",
                                       "prefix-test_upper.PCAP", "prefix-test_camel.Pcap"],

        "pcapng_filenames_with_prefix": ["prefix-test_lower.pcapng", "prefix-test_double_ending.py.pcapng",
                                         "prefix-test_upper.PCAPNG", "prefix-test_camel.Pcapng"]
    }
