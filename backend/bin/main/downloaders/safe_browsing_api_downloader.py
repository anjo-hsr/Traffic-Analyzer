import json
from typing import Union, List, Dict
from urllib import request
from urllib.error import HTTPError
from urllib.request import urlopen

from main.helpers.file import file_read_helper


class SafeBrowsingApiDownloader:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.is_api_key_correct = True

    @staticmethod
    def get_api_key() -> str:
        config_name = "traffic-analyzer.conf"
        key = "safe_browsing_api_key"
        return file_read_helper.get_config_value(config_name, key)
    
    def get_domains_threat_infomation(self, domains) -> Dict:
        if self.is_api_key_correct and domains and self.api_key != "":
            req = request.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key)
            req_data = self.generate_request_data(domains)
            req.add_header("Content-Type", "application/json")
            try:
                response = urlopen(req, json.dumps(req_data).encode("utf-8")).read()
                return json.loads(response.decode("utf-8"))
            except HTTPError:
                self.is_api_key_correct = False
                return {}

    def generate_request_data(self, filtered_domains) -> Dict[str, Dict[str, Union[List[str], str]]]:
        domain_entries = self.get_domain_entries(filtered_domains)
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
