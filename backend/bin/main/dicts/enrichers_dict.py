from collections import OrderedDict

from main.enrichers.ad_enricher import AdEnricher
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.dns_lookup_enricher import DnsLookupEnricher
from main.enrichers.ip_type_enricher import IpTypeEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.stream_enricher import StreamEnricher
from main.enrichers.tls_enricher import TlsEnricher


def get_enricher_dict() -> OrderedDict:
    return OrderedDict([
        ("location_enricher", LocationEnricher()),
        ("fqdn_resolve_enricher", NameResolverEnricher()),
        ("cipher_suite_enricher", CipherSuiteEnricher()),
        ("tls_ssl_version_enricher", TlsEnricher()),
        ("ip_type_enricher", IpTypeEnricher()),
        ("stream_enricher", StreamEnricher()),
        ("dns_lookup_enricher", DnsLookupEnricher()),
        ("ad_enricher", AdEnricher())
    ])
