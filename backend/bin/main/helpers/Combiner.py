class Combiner:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet):
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, helpers, packet):
        dst_src = Combiner.get_dst_src(packet)

        fqdn_information = helpers["name_resolver"].resolve(dst_src)
        location_information = helpers["locator"].locate(dst_src)
        cipher_suite_information = helpers["cipher_suites"].get_cipher_suite(packet)
        line = Combiner.combine_fields(
            [joined_default_cells, location_information, fqdn_information, cipher_suite_information])
        return line

    @staticmethod
    def combine_fields(fields, quotes_needed=False):
        if quotes_needed:
            return ",".join('"{}"'.format(field) for field in fields)

        return ",".join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet):
        joined_default_cells = Combiner.delimiter.join('"{}"'.format(packet[cell]) for cell in packet)
        return joined_default_cells

    @staticmethod
    def combine_fqdns(fqdns, destination, source):
        return '"{1}"{0}"{2}"'.format(Combiner.delimiter, fqdns.get(destination), fqdns.get(source))

    @staticmethod
    def combine_lat_long(locations, destination):
        return Combiner.delimiter.join('"{}"'.format(cell) for cell in locations.get(destination))
