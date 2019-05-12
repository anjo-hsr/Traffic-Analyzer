from collections import OrderedDict


def get_information_dict() -> OrderedDict[str, None]:
    return OrderedDict([
        ("location_information", None),
        ("fqdn_information", None),
        ("cipher_suite_information", None),
        ("tls_ssl_version", None),
        ("ip_type_information", None),
        ("stream_id", None),
        ("dns_lookup_information", None),
        ("ad_value", None)
    ])


def fill_dict(information_dict, fill_list) -> None:
    key_index = 0
    value_index = 1

    for tuple_entry in fill_list:
        information_dict[tuple_entry[key_index]] = tuple_entry[value_index]
