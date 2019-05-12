from main.enrichers.enricher import Enricher
from main.helpers.combine_helper import CombineHelper


class LocationEnricher(Enricher):
    def __init__(self):
        enricher_type = "location enricher"
        header = "dst_latitude,dst_longitude,src_latitude,src_longitude"
        Enricher.__init__(self, enricher_type, header)

    @staticmethod
    def extract_location(dst_src_information) -> str:
        dst_data = dst_src_information["dst"]
        src_data = dst_src_information["src"]
        dst_lat_long = [dst_data["latitude"], dst_data["longitude"]]
        src_lat_long = [src_data["latitude"], src_data["longitude"]]

        pos_dest = CombineHelper.delimiter.join('"{}"'.format(position_data) for position_data in dst_lat_long)
        pos_src = CombineHelper.delimiter.join('"{}"'.format(position_data) for position_data in src_lat_long)

        return CombineHelper.delimiter.join([pos_dest, pos_src])
