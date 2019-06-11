from collections import OrderedDict

from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_address_combine_enricher import IpAddressCombineEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.server_type_enricher import ServerTypeEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.threat_info_enricher import ThreatInfoEnricher
from main.enrichers.tls_version_enricher import TlsVersionEnricher


def get_enricher_dict() -> OrderedDict:
    return OrderedDict([
        ("ip_address_combine_enricher", IpAddressCombineEnricher()),
        ("location_enricher", LocationEnricher()),
        ("fqdn_resolve_enricher", NameResolverEnricher()),
        ("stream_enricher", StreamEnricher()),
        ("cipher_suite_enricher", CipherSuiteEnricher()),
        ("tls_ssl_version_enricher", TlsVersionEnricher()),
        ("ip_type_enricher", IpTypeEnricher()),
        ("dns_lookup_enricher", DnsLookupEnricher()),
        ("server_type_enricher", ServerTypeEnricher()),
        ("ad_enricher", AdEnricher()),
        ("threat_info_enricher", ThreatInfoEnricher())
    ])
