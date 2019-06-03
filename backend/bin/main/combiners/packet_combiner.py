from typing import Dict


class PacketCombiner:
    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_ip_versions(packet) -> None:
        packet["ip_dst_combined"] = packet["ip.dst"] + packet["ipv6.dst"]
        packet["ip_dst_combined"] = packet["ip.src"] + packet["ipv6.src"]
