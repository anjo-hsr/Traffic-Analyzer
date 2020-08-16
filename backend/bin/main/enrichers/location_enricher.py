from typing import Dict, Union, Optional

from main.enrichers.enricher import Enricher
from main.helpers.string_helper import enclose_with_quotes


class LocationEnricher(Enricher):
    def __init__(self) -> None:
        enricher_type = "location enricher"
        header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        Enricher.__init__(self, enricher_type, header)

    def get_information(self, _: Optional[Dict[str, str]],
                        information_dict: Dict[str, Union[str, Dict[str, Dict[str, str]]]]) -> None:
        dst_data = information_dict["dst_src_information"]["dst"]
        src_data = information_dict["dst_src_information"]["src"]

        information_dict["dst_latitude"] = enclose_with_quotes(dst_data["latitude"])
        information_dict["dst_longitude"] = enclose_with_quotes(dst_data["longitude"])

        information_dict["src_latitude"] = enclose_with_quotes(src_data["latitude"])
        information_dict["src_longitude"] = enclose_with_quotes(src_data["longitude"])
