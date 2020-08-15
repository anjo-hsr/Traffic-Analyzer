from typing import Dict


def get_dst_src(packet: Dict[str, str]) -> Dict[str, str]:
    ip_enumerate_character = ","
    ip_dst_key = "ip.dst"
    ip_src_key = "ip.src"
    ipv6_dst_key = "ipv6.dst"
    ipv6_src_key = "ipv6.src"

    packet[ip_dst_key] = packet[ip_dst_key].split(ip_enumerate_character)[0]
    packet[ip_src_key] = packet[ip_src_key].split(ip_enumerate_character)[0]
    packet[ipv6_dst_key] = packet[ipv6_dst_key].split(ip_enumerate_character)[0]
    packet[ipv6_src_key] = packet[ipv6_src_key].split(ip_enumerate_character)[0]

    return {
        "dst": packet[ip_dst_key] + packet[ipv6_dst_key],
        "src": packet[ip_src_key] + packet[ipv6_src_key]
    }
