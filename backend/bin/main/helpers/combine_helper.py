class CombineHelper:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet):
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, enricher, packet):
        ip_information_downloader = enricher.ip_information_downloader
        dst_src = CombineHelper.get_dst_src(packet)
        dst_src_information = ip_information_downloader.get_dst_src_information(dst_src)

        information_dict = enricher.get_information_dict(dst_src_information, packet)
        enriched_line = CombineHelper.delimiter.join(str(value) for value in information_dict.values())
        return CombineHelper.combine_fields([joined_default_cells, enriched_line])

    @staticmethod
    def combine_fields(fields, quotes_needed=False):
        if quotes_needed:
            return CombineHelper.delimiter.join('"{}"'.format(field) for field in fields)

        return CombineHelper.delimiter.join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet, field_names):
        return CombineHelper.delimiter.join('"{}"'.format(packet[field_name]) for field_name in field_names)

    @staticmethod
    def join_with_quotes(fields):
        return '"' + CombineHelper.delimiter.join(fields) + '"'
