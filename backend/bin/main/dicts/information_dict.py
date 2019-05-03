from collections import OrderedDict


class InformationDict:
    def __init__(self):
        self.information_dict = OrderedDict([
            ("location_information", None),
            ("fqdn_information", None),
            ("cipher_suite_information", None),
            ("tls_ssl_version", None),
            ("ip_type_information", None),
            ("stream_id", None),
            ("dns_lookup_information", None),
            ("ad_value", None)
        ])

    def fill_dict(self, fill_list):
        key_index = 0
        value_index = 1

        for tuple_entry in fill_list:
            self.information_dict[tuple_entry[key_index]] = tuple_entry[value_index]
