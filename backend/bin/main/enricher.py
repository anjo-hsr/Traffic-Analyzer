from collections import OrderedDict

from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ad_enricher import AdEnricher
from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.tls_enricher import TlsEnricher
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class Enricher:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.limiter = limiter
        self.enrichers = None
        self.ip_information_downloader = None
        self.initialize_variables()

    def reset_variables(self):
        self.initialize_variables()

    def initialize_variables(self):
        self.enrichers = OrderedDict([
            ("location_enricher", LocationEnricher()),
            ("name_resolve_enricher", NameResolverEnricher()),
            ("cipher_suite_enricher", CipherSuiteEnricher()),
            ("tls_ssl_version_enricher", TlsEnricher()),
            ("ip_type_enricher", IpTypeEnricher()),
            ("stream_enricher", StreamEnricher()),
            ("ad_enricher", AdEnricher()),
            ("dns_lookup_enricher", DnsLookupEnricher())
        ])
        self.ip_information_downloader = IpInformationDownloader(self.limiter)
