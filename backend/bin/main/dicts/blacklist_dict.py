from typing import List

import requests
from bs4 import BeautifulSoup


class BlacklistDict:
    def __init__(self, blacklist_domains) -> None:
        self.blacklist_dict = {}

        if blacklist_domains is None:
            blacklist_domains = self.get_blacklist_domains()

        self.generate_blacklist_dict(blacklist_domains)

    @staticmethod
    def get_blacklist_domains() -> List[str]:
        url = "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=plain;showintro=0"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return [url for url in soup.pre.text.split("\n") if url != ""]

    def generate_blacklist_dict(self, blacklist_domains) -> None:
        for domain in blacklist_domains:
            domain_parts = domain.split(".")
            start_index = len(domain_parts) - 1
            dict_to_write = self.blacklist_dict
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

        dict_entry = self.blacklist_dict.get(key, {})
        dict_entry[value] = next_value
        dict_to_write[key] = dict_entry

        domain_parts = domain_parts[:index]
        self.write_domain_into_dict(dict_entry, domain_parts, domain, index - 1)
