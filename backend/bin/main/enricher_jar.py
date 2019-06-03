from collections import OrderedDict

from main.combiners.packet_combiner import PacketCombiner
from main.dicts.enrichers_dict import get_enricher_dict
from main.downloaders.ip_information_downloader import IpInformationDownloader
from main.helpers.traffic_limit_helper import TrafficLimitHelper


class EnricherJar:
    def __init__(self, limiter=TrafficLimitHelper(2, 1)):
        self.limiter = limiter
        self.enricher_classes = get_enricher_dict()
        self.enricher_headers = []
        self.ip_information_downloader = IpInformationDownloader(limiter)

    def reset_variables(self) -> None:
        self.enricher_classes = get_enricher_dict()
        self.ip_information_downloader = IpInformationDownloader(self.limiter)

    def get_information_dict(self, packet) -> OrderedDict:
        information_dict = self.create_information_dict(packet)

        if not information_dict and not packet:
            return information_dict

        for enricher_class in self.enricher_classes:
            self.enricher_classes[enricher_class].get_information(packet, information_dict)

        return information_dict

    def create_information_dict(self, packet) -> OrderedDict:
        ip_information_downloader = self.ip_information_downloader
        dst_src = PacketCombiner.get_dst_src(packet)
        information_dict = OrderedDict([
            ("dst_src_information", ip_information_downloader.get_dst_src_information(dst_src))
        ])
        return information_dict
