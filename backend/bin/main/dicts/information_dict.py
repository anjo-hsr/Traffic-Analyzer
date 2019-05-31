from collections import OrderedDict


def get_information_dict() -> OrderedDict:
    return OrderedDict([
        ("location_information", None),
        ("fqdn_information", None),
        ("cipher_suite_information", None),
        ("tls_ssl_version", None),
        ("ip_type_information", None),
        ("stream_id", None),
        ("dns_lookup_information", None),
        ("server_types", None),
        ("ad_value", None),
        ("threat_information", None)
    ])
