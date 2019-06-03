from typing import Dict


class PacketCombiner:
    ip_enumerate_character = ","

    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        dst_src = {
            "dst": packet["ip_dst_combined"],
            "src": packet["ip_src_combined"]
        }
        return dst_src

    @staticmethod
    def combine_ip_versions(packet) -> None:
        packet["ip.dst"] = packet["ip.dst"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ip.src"] = packet["ip.src"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ipv6.dst"] = packet["ipv6.dst"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ipv6.src"] = packet["ipv6.src"].split(PacketCombiner.ip_enumerate_character)[0]

        packet["ip_dst_combined"] = packet["ip.dst"] + packet["ipv6.dst"]
        packet["ip_src_combined"] = packet["ip.src"] + packet["ipv6.src"]
