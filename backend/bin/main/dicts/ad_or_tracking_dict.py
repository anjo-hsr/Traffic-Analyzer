import socket
import time
from typing import List

import requests
from bs4 import BeautifulSoup


class AdOrTrackingDict(object):
    def __init__(self, ad_or_tracking_domains) -> None:
        self.ad_or_tracking_dict = {}

        if ad_or_tracking_domains is None:
            ad_or_tracking_domains = self.get_ad_or_tracking_domains()

        self.generate_ad_or_tracking_dict(ad_or_tracking_domains)

    @staticmethod
    def get_ad_or_tracking_domains(counter=0) -> List[str]:
        try:
            url = "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=plain;showintro=0"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                return [url for url in soup.pre.text.split("\n") if url != ""]

        except (socket.gaierror, requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            if counter < 5:
                time.sleep(2)
                return AdOrTrackingDict.get_ad_or_tracking_domains(counter + 1)

        return []

    def generate_ad_or_tracking_dict(self, ad_or_tracking_domains) -> None:
        for domain in ad_or_tracking_domains:
            domain_parts = domain.split(".")
            start_index = len(domain_parts) - 1
            dict_to_write = self.ad_or_tracking_dict
            self.write_domain_into_dict(dict_to_write, domain_parts, domain, start_index)

    def write_domain_into_dict(self, dict_to_write, domain_parts, domain, index) -> None:
        if index < 1:
            return

        if index < 2:
            next_value = domain
        else:
            next_value = {}

        key = domain_parts[index]
        value = domain_parts[index - 1]

        dict_entry = self.ad_or_tracking_dict.get(key, {})
        dict_entry[value] = next_value
        dict_to_write[key] = dict_entry

        domain_parts = domain_parts[:index]
        self.write_domain_into_dict(dict_entry, domain_parts, domain, index - 1)
