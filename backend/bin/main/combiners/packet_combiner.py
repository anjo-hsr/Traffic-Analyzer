from typing import Dict


class PacketCombiner:
    @staticmethod
    def get_dst_src(packet) -> Dict[str, str]:
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src
