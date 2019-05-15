from collections import OrderedDict

from main.dicts.enrichers_dict import get_enricher_dict
from main.dicts.information_dict import get_information_dict, fill_dict
from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class EnricherJar:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.limiter = limiter
        self.enricher_classes = get_enricher_dict()
        self.information_dict = get_information_dict()
        self.ip_information_downloader = IpInformationDownloader(limiter)

    def reset_variables(self) -> None:
        self.enricher_classes = get_enricher_dict()
        self.information_dict = get_information_dict()
        self.ip_information_downloader = IpInformationDownloader(self.limiter)

    def get_information_dict(self, dst_src_information, packet) -> OrderedDict:
        if dst_src_information is None and packet is None:
            return self.information_dict

        location_information = self.enricher_classes["location_enricher"].extract_location(dst_src_information)
        fqdn_information = self.enricher_classes["fqdn_resolve_enricher"].extract_fqdn(dst_src_information)
        cipher_suite_information = self.enricher_classes["cipher_suite_enricher"].get_cipher_suite(packet)
        tls_ssl_version = self.enricher_classes["tls_ssl_version_enricher"].get_tls_ssl_version(packet)
        ip_type_information = self.enricher_classes["ip_type_enricher"].extract_ip_types(dst_src_information)
        stream_id = self.enricher_classes["stream_enricher"].get_stream_id(packet)
        dns_lookup_information = self.enricher_classes["dns_lookup_enricher"].detect_dns_request(packet, stream_id)
        ad_value = self.enricher_classes["ad_enricher"].test_domains(dns_lookup_information)
        threat_type = self.enricher_classes["threat_info_enricher"].test_domains_threats(dns_lookup_information)

        fill_dict(self.information_dict, [
            ("location_information", location_information),
            ("fqdn_information", fqdn_information),
            ("cipher_suite_information", cipher_suite_information),
            ("tls_ssl_version", tls_ssl_version),
            ("ip_type_information", ip_type_information),
            ("stream_id", stream_id),
            ("dns_lookup_information", dns_lookup_information),
            ("ad_value", ad_value),
            ("threat_information", threat_type)
        ])

        return self.information_dict
