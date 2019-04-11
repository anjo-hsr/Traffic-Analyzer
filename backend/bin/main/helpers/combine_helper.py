class CombineHelper:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet):
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, enrichers, packet):
        dst_src = CombineHelper.get_dst_src(packet)

        fqdn_information = enrichers["name_resolve_enricher"].resolve(dst_src)
        location_information = enrichers["location_enricher"].locate(dst_src)
        cipher_suite_information = enrichers["cipher_suite_enricher"].get_cipher_suite(packet)
        tls_ssl_version = enrichers["tls_ssl_version_enricher"].get_tls_ssl_version(packet)
        protocol = enrichers["protocol_enricher"].get_protocol(packet)
        line = CombineHelper.combine_fields(
            [joined_default_cells, location_information, fqdn_information,
             cipher_suite_information, tls_ssl_version, protocol])
        return line

    @staticmethod
    def combine_fields(fields, quotes_needed=False):
        if quotes_needed:
            return ",".join('"{}"'.format(field) for field in fields)

        return ",".join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet):
        joined_default_cells = CombineHelper.delimiter.join('"{}"'.format(packet[cell]) for cell in packet)
        return joined_default_cells

    @staticmethod
    def combine_fqdns(fqdns, destination, source):
        return '"{1}"{0}"{2}"'.format(CombineHelper.delimiter, fqdns.get(destination), fqdns.get(source))

    @staticmethod
    def combine_lat_long(locations, destination):
        return CombineHelper.delimiter.join('"{}"'.format(cell) for cell in locations.get(destination))