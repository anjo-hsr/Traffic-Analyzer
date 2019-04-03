import unittest

import bin.main.helpers.Tshark as Tshark


class TestTsharkMethods(unittest.TestCase):
    def test_tshark_get_arguments(self):
        filename = "test.pcap"
        args = ['-r', filename, '-T', 'fields', '-e', 'frame.time', '-e', 'frame.cap_len', '-e',
                'eth.dst', '-e', 'eth.src',
                '-e', 'ip.dst', '-e', 'ip.src', '-e', 'ip.proto', '-e',
                'tcp.srcport', '-e', 'tcp.dstport', '-e', 'tcp.flags', '-e', 'tcp.len', '-e',
                'udp.srcport', '-e', 'udp.srcport', '-e', 'udp.length',
                '-E', 'header=y', '-E', 'separator=,', '-E', 'quote=d', '-E', 'occurrence=f']

        self.assertEqual(Tshark.get_arguments(filename), args)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTsharkMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
