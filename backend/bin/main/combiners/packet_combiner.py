from typing import Dict


def get_dst_src(packet) -> Dict[str, str]:
    ip_enumerate_character = ","
    packet["ip.dst"] = packet["ip.dst"].split(ip_enumerate_character)[0]
    packet["ip.src"] = packet["ip.src"].split(ip_enumerate_character)[0]
    packet["ipv6.dst"] = packet["ipv6.dst"].split(ip_enumerate_character)[0]
    packet["ipv6.src"] = packet["ipv6.src"].split(ip_enumerate_character)[0]

    return {
        "dst": packet["ip.dst"] + packet["ipv6.dst"],
        "src": packet["ip.src"] + packet["ipv6.src"]
    }
