import json
from typing import Union, List, Dict, Set
from urllib import request
from urllib.error import HTTPError
from urllib.request import urlopen

from main.combiners.field_combiner import FieldCombiner
from main.enrichers.enricher import Enricher
from main.helpers.file import file_read_helper
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
        self.api_key = self.get_api_key()
        self.is_api_key_correct = True

    @staticmethod
    def get_api_key() -> str:
        config_name = "traffic-analyzer.conf"
        key = "safe_browsing_api_key"
        return file_read_helper.get_config_value(config_name, key)

    def get_information(self, packet, information_dict) -> None:
        domain_array = information_dict["domains"].split(",")
        domain_array = list(map(remove_quotations, domain_array))

        if all(domain == "" for domain in domain_array):
            information_dict["threat_category"] = '""'
            return

        filtered_domains = list(filter(lambda domain: domain not in self.threat_dict, domain_array))
        for domain in filtered_domains:
            self.threat_dict[domain] = ""

        self.get_domains_threat_infomation(filtered_domains)
        matched_threat_types = self.reduce_threat_information(domain_array)
        threat_numbers = list(map(self.get_threat_number, matched_threat_types))
        information_dict["threat_category"] = FieldCombiner.join_with_quotes(threat_numbers)

    def get_domains_threat_infomation(self, domains) -> None:
        if self.is_api_key_correct and domains and self.api_key != "":
            req = request.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key)
            req_data = self.generate_request_data(domains)
            req.add_header("Content-Type", "application/json")
            try:
                response = urlopen(req, json.dumps(req_data).encode("utf-8")).read()
                response_dict = json.loads(response.decode("utf-8"))
                self.update_threat_dict(response_dict)
            except HTTPError:
                self.is_api_key_correct = False

    @staticmethod
    def generate_request_data(filtered_domains) -> Dict[str, Dict[str, Union[List[str], str]]]:
        domain_entries = ThreatInfoEnricher.get_domain_entries(filtered_domains)
        return {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": domain_entries
            }
        }

    @staticmethod
    def get_domain_entries(filtered_domains) -> List[Dict[str, str]]:
        return list(map(lambda domain: {"url": domain}, filtered_domains))

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
