from typing import Dict, Union, Optional

from main.enrichers.enricher import Enricher
from main.helpers.string_helper import enclose_with_quotes


class NameResolverEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "name resolve enricher"
        header = "dst_fqdn,src_fqdn"
        Enricher.__init__(self, enricher_type, header)

    def get_information(self, _: Optional[Dict[str, str]],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        dst_data = information_dict["dst_src_information"]["dst"]
        src_data = information_dict["dst_src_information"]["src"]
        information_dict["dst_fqdn"] = enclose_with_quotes(dst_data["rdns"])
        information_dict["src_fqdn"] = enclose_with_quotes(src_data["rdns"])
