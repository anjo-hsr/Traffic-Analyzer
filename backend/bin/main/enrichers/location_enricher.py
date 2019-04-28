from main.helpers.combine_helper import CombineHelper
from main.helpers.print_helper import PrintHelper


class LocationEnricher:
    def __init__(self):
        self.header = "dst_latitude,dst_longitude,src_latitude,src_longitude"

    @staticmethod
    def extract_location(dst_src_information):
        dst_data = dst_src_information["dst"]
        src_data = dst_src_information["src"]
        dst_lat_long = [dst_data["latitude"], dst_data["longitude"]]
        src_lat_long = [src_data["latitude"], src_data["longitude"]]

        pos_dest = CombineHelper.delimiter.join('"{}"'.format(position_data) for position_data in dst_lat_long)
        pos_src = CombineHelper.delimiter.join('"{}"'.format(position_data) for position_data in src_lat_long)

        return CombineHelper.delimiter.join([pos_dest, pos_src])

    def print(self):
        enricher_type = "location enricher"
        PrintHelper.print_nothing(enricher_type)
