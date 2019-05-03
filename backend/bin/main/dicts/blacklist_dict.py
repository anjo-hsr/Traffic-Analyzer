import requests
from bs4 import BeautifulSoup


class BlacklistDict:
    def __init__(self, blacklist_urls):
        self.blacklist_dict = {}

        if blacklist_urls is None:
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
            self.write_url_into_dict(dict_to_write, url_parts, url, start_index)

    def write_url_into_dict(self, dict_to_write, url_parts, url, index):
        if index < 1:
            return

        if index < 2:
            next_value = url
        else:
            next_value = {}

        key = url_parts[index]
        value = url_parts[index - 1]

        dict_entry = self.blacklist_dict.get(key, {})
        dict_entry[value] = next_value
        dict_to_write[key] = dict_entry

        url_parts = url_parts[:index]
        self.write_url_into_dict(dict_entry, url_parts, url, index - 1)
