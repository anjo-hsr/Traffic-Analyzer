import json
from os import path
from urllib import request
from urllib.error import HTTPError
from urllib.request import urlopen

from main.helpers.combine_helper import CombineHelper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_read_helper


class ThreatInfoEnricher:
    def __init__(self):
        self.header = "threat_type"
        self.threat_dict = {"": ""}
        self.threat_type_dict = {
            "": "",
            "THREAT_TYPE_UNSPECIFIED": "2",
            "MALWARE": "3",
            "SOCIAL_ENGINEERING": "4",
            "UNWANTED_SOFTWARE": "5",
            "POTENTIALLY_HARMFUL_APPLICATION": "6"
        }
        self.api_key = self.get_api_key()
        self.is_api_key_correct = True

    @staticmethod
    def get_api_key():
        environment = EnvironmentHelper().get_environment()
        config_file = "traffic-analyzer.conf"
        key = "safe_browsing_api_key"
        file_path = path.join(environment["configuration_folder"], config_file)
        return file_read_helper.get_config_value(file_path, key)

    def test_urls_threats(self, urls):
        url_array = urls.split(",")
        url_array = list(map(self.remove_quotations, url_array))

        if all(url == "" for url in url_array):
            return ""

        filtered_urls = list(filter(lambda url: url not in self.threat_dict, url_array))
        for url in filtered_urls:
            self.threat_dict[url] = ""

        matched_threat_types = self.get_urls_threat_infomation(filtered_urls)
        threat_numbers = list(map(self.get_threat_number, matched_threat_types))
        return CombineHelper.join_with_quotes(threat_numbers)

    def get_urls_threat_infomation(self, urls):
        if self.is_api_key_correct and urls and self.api_key != "":
            req = request.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key)
            req_data = self.generate_request_data(urls)
            req.add_header('Content-Type', 'application/json')
            print(req_data)
            try:
                response = urlopen(req, json.dumps(req_data).encode("utf-8")).read()
                response_dict = json.loads(response.decode("utf-8"))
                self.update_threat_dict(response_dict)
            except HTTPError:
                self.is_api_key_correct = False

        return self.reduce_threat_information(urls)

    @staticmethod
    def generate_request_data(filtered_urls):
        url_entries = ThreatInfoEnricher.get_url_entries(filtered_urls)
        return {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": url_entries
            }
        }

    @staticmethod
    def get_url_entries(filtered_urls):
        return list(map(lambda url: {"url": url}, filtered_urls))

    def update_threat_dict(self, response_dict):
        if response_dict == {}:
            return

        for match in response_dict["matches"]:
            url = match["threat"]["url"]
            threat_type = match["threatType"]
            self.threat_dict[url] = threat_type

    def reduce_threat_information(self, urls):
        reduced_list = set()
        for url in urls:
            if url != "" and url in self.threat_dict:
                for threatType in self.threat_dict[url].split(","):
                    reduced_list.add(threatType)

        return reduced_list

    def get_threat_number(self, threat_string_entry):
        return self.threat_type_dict[threat_string_entry]

    @staticmethod
    def remove_quotations(url):
        return url.replace('"', "").replace("'", "")

    def print(self):
        pass
