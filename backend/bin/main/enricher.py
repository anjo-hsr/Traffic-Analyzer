from main.dicts.enrichers_dict import EnrichersDict
from main.dicts.information_dict import InformationDict
from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class Enricher:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.limiter = limiter
        self.enricher_classes = EnrichersDict()
        self.ip_information_downloader = IpInformationDownloader(limiter)
        self.initialize_variables()
        self.information_dict = InformationDict()

    def reset_variables(self):
        self.initialize_variables()

    def initialize_variables(self):
        self.enricher_classes = EnrichersDict()
        self.ip_information_downloader = IpInformationDownloader(self.limiter)

    def get_information_dict(self, dst_src_information, packet):
        if dst_src_information is None and packet is None:
            return self.information_dict.information_dict

        enrichers_dict = self.enricher_classes.enrichers_dict
        location_information = enrichers_dict["location_enricher"].extract_location(dst_src_information)
        fqdn_information = enrichers_dict["name_resolve_enricher"].extract_fqdn(dst_src_information)
        cipher_suite_information = enrichers_dict["cipher_suite_enricher"].get_cipher_suite(packet)
        tls_ssl_version = enrichers_dict["tls_ssl_version_enricher"].get_tls_ssl_version(packet)
        ip_type_information = enrichers_dict["ip_type_enricher"].extract_ip_types(dst_src_information)
        stream_id = enrichers_dict["stream_enricher"].get_stream_id(packet)
        dns_lookup_information = enrichers_dict["dns_lookup_enricher"].detect_dns_request(packet, stream_id)
        ad_value = enrichers_dict["ad_enricher"].test_urls(dns_lookup_information)

        self.information_dict.fill_dict([
            ("location_information", location_information),
            ("fqdn_information", fqdn_information),
            ("cipher_suite_information", cipher_suite_information),
            ("tls_ssl_version", tls_ssl_version),
            ("ip_type_information", ip_type_information),
            ("stream_id", stream_id),
            ("dns_lookup_information", dns_lookup_information),
            ("ad_value", ad_value)
        ])

        return self.information_dict.information_dict
