import requests

from bs4 import BeautifulSoup

from main.helpers.ip_helper import IpHelper


class AdEnricher:

    def __init__(self):
        self.ip_to_category = {}
        self.header = "is_ad"
        self.blacklist_dict = {}
        self.url_to_ad_dict = {}
        blacklist_urls = self.get_blacklist_urls()
        self.generate_blacklist_dict(blacklist_urls)

    @staticmethod
    def get_blacklist_urls():
        url = "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=plain;showintro=0"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [url for url in soup.pre.text.split("\n") if url != ""]

    def generate_blacklist_dict(self, blacklist_urls):
        for url in blacklist_urls:
            url_parts = url.split(".")
            start_index = len(url_parts) - 1
            dict_to_write = self.blacklist_dict
            self.write_url_into_dict(dict_to_write, url_parts, start_index)

    def write_url_into_dict(self, dict_to_write, url_parts, index):
        if index < 1:
            return

        key = url_parts[index]
        value = url_parts[index - 1]

        dict_entry = self.blacklist_dict.get(key, {})
        dict_entry[value] = {}
        dict_to_write[key] = dict_entry

        url_parts = url_parts[:index]
        self.write_url_into_dict(dict_entry, url_parts, index - 1)

    def test_url(self, url):
        url = url.replace('"', '')
        url = url.replace("'", "")

        if url in self.url_to_ad_dict:
            return self.url_to_ad_dict[url]

        is_ad = False
        dict_to_test = self.blacklist_dict

        if not IpHelper.is_ip(url):
            reversed_url_parts = reversed(url.split("."))
            for index, url_part in enumerate(reversed_url_parts):
                dict_to_test = self.test_url_part(url_part, dict_to_test)
                if index < 2 and dict_to_test == {}:
                    self.url_to_ad_dict[url] = False
                    return False

        is_ad = is_ad or dict_to_test == {}
        self.url_to_ad_dict[url] = is_ad
        return is_ad

    @staticmethod
    def test_url_part(url_part, current_dict):
        return current_dict.get(url_part, {})

    def test_urls(self, fqdn_information):
        destination, source = fqdn_information.split(",")
        is_ad = self.test_url(destination) or self.test_url(source)

        return str(is_ad)

    def print(self):
        pass
