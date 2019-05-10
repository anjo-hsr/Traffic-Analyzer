import json
from os import path
from urllib import request
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

        filtered_urls = list(filter(self.is_url_not_in_dict, url_array))
        for url in filtered_urls:
            self.threat_dict[url] = ""

        matched_threat_types = self.get_urls_threat_infomation(filtered_urls)
        threat_numbers = list(map(self.get_threat_number, matched_threat_types))
        return CombineHelper.join_with_quotes(threat_numbers)

    def get_urls_threat_infomation(self, urls):
        if urls and self.api_key != "":
            print("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key)
            req = request.Request("https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + self.api_key)
            req_data = self.generate_request_data(urls)
            req.add_header('Content-Type', 'application/json')
            response = urlopen(req, json.dumps(req_data).encode("utf-8")).read()
            response_dict = json.loads(response)
            self.update_threat_dict(response_dict)

        return self.reduce_threat_information(urls)

    def is_url_not_in_dict(self, url):
        return url not in self.threat_dict

    @staticmethod
    def generate_request_data(filtered_urls):
        threat_entries = list(map(ThreatInfoEnricher.generate_url_entry, filtered_urls))
        print(threat_entries)
        return {
            "threatInfo": {
                "threatTypes": ["THREAT_TYPE_UNSPECIFIED", "MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE",
                                "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": threat_entries
            }
        }

    @staticmethod
    def generate_url_entry(url):
        return {"url": url}

    def update_threat_dict(self, response_dict):
        if response_dict == {}:
            return

        for match in response_dict["matches"]:
            url = match["threat"]["url"]
            threat_type = match["threatType"]
            self.threat_type_dict[url] = threat_type

    def reduce_threat_information(self, urls):
        reduced_list = set()
        for url in urls:
            if url != "" and url in self.threat_type_dict:
                for threatType in self.threat_type_dict[url].split(","):
                    reduced_list.add(threatType)

        return reduced_list

    def get_threat_number(self, threat_string_entry):
        return self.threat_type_dict[threat_string_entry]

    @staticmethod
    def remove_quotations(url):
        url = url.replace('"', '')
        url = url.replace("'", "")
        return url

    def print(self):
        pass
