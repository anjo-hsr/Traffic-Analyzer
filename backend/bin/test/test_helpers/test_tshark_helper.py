import unittest

from main.helpers.tshark_helper import get_arguments


class TestTsharkHelperMethods(unittest.TestCase):
    def test_tshark_get_arguments(self) -> None:
        filename = "test.pcap"
        args = ["-r", filename, "-T", "fields",
                "-e", "frame.time", "-e", "frame.len",
                "-e", "_ws.col.Protocol",
                "-e", "eth.dst", "-e", "eth.src",
                "-e", "ip.dst", "-e", "ip.src", "-e", "ip.proto",
                "-e", "ipv6.dst", "-e", "ipv6.src",
                "-e", "tcp.srcport", "-e", "tcp.dstport", "-e", "tcp.flags", "-e", "tcp.len", "-e", "tcp.stream",
                "-e", "udp.srcport", "-e", "udp.dstport", "-e", "udp.length",
                "-e", "dhcp.option.dhcp",
                "-e", "dns.flags.response", "-e", "dns.qry.name",
                "-e", "dns.a", "-e", "dns.aaaa", "-e", "dns.resp.name", "-e", "dns.resp.type",
                "-e", "http.request.method", "-e", "http.request.uri",
                "-e", "tls.handshake.version", "-e", "tls.handshake.extensions.supported_version",
                "-e", "tls.handshake.ciphersuite", "-e", "tls.handshake.type",
                "-E", "header=y", "-E", "separator=,", "-E", "quote=d", "-E", "occurrence=a"]

        self.assertEqual(get_arguments(filename), args)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTsharkHelperMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
