class Combiner:
    delimiter = ","

    @staticmethod
    def get_src_dst(packet):
        dst_ip_addr = packet["ip.dst"]
        src_ip_addr = packet["ip.src"]
        src_dst = [dst_ip_addr, src_ip_addr]
        return src_dst

    @staticmethod
    def combine_packet_information(joined_default_cells, helpers, packet):
        src_dst = Combiner.get_src_dst(packet)

        fqdn_information = helpers["name_resolver"].resolve(src_dst)
        location_information = helpers["locator"].locate(src_dst)
        cipher_suite_information = helpers["cipher_suites"].get_cipher_suite(packet)
        line = Combiner.combine_fields(
            [joined_default_cells, location_information, fqdn_information, cipher_suite_information])
        return line

    @staticmethod
    def combine_fields(fields, quotes_needed=False):
        if quotes_needed:
            return ",".join('"{}"'.format(field) for field in fields)

        else:
            return ",".join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet, csv_delimiter):
        joined_default_cells = csv_delimiter.join('"{}"'.format(packet[cell]) for cell in packet)
        return joined_default_cells

    @staticmethod
    def combine_fqdns(fqdns, destination, source):
        return '"{1}"{0}"{2}"'.format(Combiner.delimiter, fqdns.get(destination), fqdns.get(source))

    @staticmethod
    def combine_lat_long(locations, destination):
        return Combiner.delimiter.join('"{}"'.format(cell) for cell in locations.get(destination))
