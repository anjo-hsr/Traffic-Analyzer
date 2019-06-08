from typing import Set

from main.combiners.field_combiner import FieldCombiner
from main.downloaders.safe_browsing_api_downloader import SafeBrowsingApiDownloader
from main.enrichers.enricher import Enricher
from main.helpers.string_helper import remove_quotations


class ThreatInfoEnricher(Enricher):
    def __init__(self) -> None:
        header = "threat_category"
        enricher_type = "threat enricher"
        Enricher.__init__(self, enricher_type, header)

        self.threat_dict = {"": ""}
        self.threat_type_dict = {
            "": "",
            "THREAT_TYPE_UNSPECIFIED": "1",
            "MALWARE": "2",
            "SOCIAL_ENGINEERING": "3",
            "UNWANTED_SOFTWARE": "4",
            "POTENTIALLY_HARMFUL_APPLICATION": "5"
        }
        self.safe_browsing_api_downloader = SafeBrowsingApiDownloader()

    def get_information(self, packet, information_dict) -> None:
        domain_array = information_dict["domains"].split(",")
        domain_array = list(map(remove_quotations, domain_array))

        if all(domain == "" for domain in domain_array):
            information_dict["threat_category"] = '""'
            return

        filtered_domains = list(filter(lambda domain: domain not in self.threat_dict, domain_array))
        for domain in filtered_domains:
            self.threat_dict[domain] = ""

        response_dict = self.safe_browsing_api_downloader.get_domains_threat_infomation(filtered_domains)
        self.update_threat_dict(response_dict)

        matched_threat_types = self.reduce_threat_information(domain_array)
        threat_numbers = list(map(self.get_threat_number, matched_threat_types))
        information_dict["threat_category"] = FieldCombiner.join_with_quotes(threat_numbers)

    def update_threat_dict(self, response_dict) -> None:
        if not response_dict:
            return

        for match in response_dict["matches"]:
            domain = match["threat"]["url"]
            threat_type = match["threatType"]
            self.threat_dict[domain] = threat_type

    def reduce_threat_information(self, domains) -> Set[str]:
        reduced_list = set()
        for domain in domains:
            if domain != "" and domain in self.threat_dict:
                for threat_type in self.threat_dict[domain].split(","):
                    reduced_list.add(threat_type)

        return reduced_list

    def get_threat_number(self, threat_string_entry) -> str:
        return self.threat_type_dict[threat_string_entry]
