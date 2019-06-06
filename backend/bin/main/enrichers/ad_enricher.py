from main.dicts.ad_or_tracking_dict import AdOrTrackingDict
from main.enrichers.enricher import Enricher
from main.helpers.ip_address_helper import IpAddressHelper
from main.helpers.string_helper import remove_quotations


class AdEnricher(Enricher):
    def __init__(self, ad_or_tracking_domains=None) -> None:
        enricher_type = "ad enricher"
        header = "ad_category"
        Enricher.__init__(self, enricher_type, header)

        self.ip_to_category = {}
        self.ad_or_tracking_dict = AdOrTrackingDict(ad_or_tracking_domains)
        self.domain_to_ad_dict = {}

    def get_information(self, packet, information_dict) -> None:
        domain_list = information_dict["domains"].split(",")
        is_ad = False
        for domain in domain_list:
            if domain == "":
                continue

            domain = remove_quotations(domain)
            is_ad = is_ad or self.is_ad_domain(domain)

        information_dict["ad_category"] = "1" if is_ad else "0"

    def is_ad_domain(self, domain) -> bool:
        if domain in self.domain_to_ad_dict:
            return self.domain_to_ad_dict[domain]

        dict_to_test = self.ad_or_tracking_dict.ad_or_tracking_dict
        is_ad = self.is_domain_in_dict(domain, dict_to_test)

        is_ad = is_ad or not dict_to_test
        self.domain_to_ad_dict[domain] = is_ad
        return is_ad

    def is_domain_in_dict(self, domain, dict_to_test) -> bool:
        return_value = False

        if IpAddressHelper.is_ip(domain):
            return return_value

        for domain_part in reversed(domain.split(".")):
            dict_value = dict_to_test.get(domain_part, {})
            if isinstance(dict_value, dict):
                if not dict_value:
                    break

                dict_to_test = dict_value

            if isinstance(dict_value, str):
                return_value = True
                break

        self.domain_to_ad_dict[domain] = return_value
        return return_value
