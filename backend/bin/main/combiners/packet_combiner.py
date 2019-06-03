from typing import Dict


class PacketCombiner:
    ip_enumerate_character = ","

    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        packet["ip.dst"] = packet["ip.dst"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ip.src"] = packet["ip.src"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ipv6.dst"] = packet["ipv6.dst"].split(PacketCombiner.ip_enumerate_character)[0]
        packet["ipv6.src"] = packet["ipv6.src"].split(PacketCombiner.ip_enumerate_character)[0]

        return {
            "dst": packet["ip.dst"] + packet["ipv6.dst"],
            "src": packet["ip.src"] + packet["ipv6.src"]
        }
