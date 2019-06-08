import json
import socket
import time
from typing import Union, List, Dict

import requests

from main.helpers.file import file_read_helper


class SafeBrowsingApiDownloader:
    def __init__(self) -> None:
        self.api_key = self.get_api_key()
        self.is_api_key_correct = self.api_key != ""

    @staticmethod
    def get_api_key() -> str:
        config_name = "traffic-analyzer.conf"
        key = "safe_browsing_api_key"
        return file_read_helper.get_config_value(config_name, key)

    def get_domains_threat_information(self, domains, counter=0) -> \
            Dict[str, List[Dict[str, Union[str, Dict[str, str]]]]]:
        if self.is_api_key_correct and domains and self.api_key != "":
            request_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key
            request_data = self.generate_request_data(domains)
            request_headers = {"Content-Type": "application/json"}
            try:
                response = requests.post(request_url, json=request_data, headers=request_headers)
                if response.status_code == 200:
                    return json.loads(response.content.decode("utf-8"))

                self.is_api_key_correct = False

            except socket.gaierror:
                if counter < 5:
                    time.sleep(2)
                    SafeBrowsingApiDownloader.get_domains_threat_information(domains, counter + 1)
        return {}

    def generate_request_data(self, domains) -> Dict[str, Dict[str, Union[List[str], str]]]:
        domain_entries = self.get_domain_entries(domains)
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
