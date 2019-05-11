from main.dicts.blacklist_dict import BlacklistDict
from main.helpers.ip_helper import IpHelper
from main.helpers.print_helper import PrintHelper


class AdEnricher:
    def __init__(self, blacklist_urls=None):
        self.enricher_type = "ad_enricher"
        self.header = "category"
        self.ip_to_category = {}
        self.blacklist_dict = BlacklistDict(blacklist_urls)
        self.url_to_ad_dict = {}

    def print(self) -> None:
        PrintHelper.print_nothing(self.enricher_type)

    def test_urls(self, urls) -> str:
        url_array = urls.split(",")
        is_ad = False
        for url in url_array:
            if url == "":
                continue

            url = self.remove_quotations(url)
            is_ad = is_ad or self.test_url(url)

        return "1" if is_ad else "0"

    def test_url(self, url) -> bool:
        if url in self.url_to_ad_dict:
            return self.url_to_ad_dict[url]

        dict_to_test = self.blacklist_dict.blacklist_dict
        is_ad = self.is_url_in_dict(url, dict_to_test)

        is_ad = is_ad or dict_to_test == {}
        self.url_to_ad_dict[url] = is_ad
        return is_ad

    @staticmethod
    def remove_quotations(url) -> str:
        url = url.replace('"', '')
        url = url.replace("'", "")
        return url

    def is_url_in_dict(self, url, dict_to_test) -> bool:
        return_value = False

        if IpHelper.is_ip(url):
            return return_value

        for url_part in reversed(url.split(".")):
            return_value = dict_to_test.get(url_part, {})
            if isinstance(return_value, dict):
                if return_value == {}:
                    break

                dict_to_test = return_value

            if isinstance(return_value, str):
                return_value = True
                break

        self.url_to_ad_dict[url] = return_value
        return return_value
