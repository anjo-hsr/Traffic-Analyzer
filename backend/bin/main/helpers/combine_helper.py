class CombineHelper:
    delimiter = ","

    @staticmethod
    def get_dst_src(packet):
        dst_src = {"dst": packet["ip.dst"], "src": packet["ip.src"]}
        return dst_src

    @staticmethod
    def combine_packet_information(joined_default_cells, enrichment_classes, packet):
        enrichers = enrichment_classes.enrichers
        ip_information_downloader = enrichment_classes.ip_information_downloader
        dst_src = CombineHelper.get_dst_src(packet)
        dst_src_information = ip_information_downloader.get_dst_src_information(dst_src)

        location_information = enrichers["location_enricher"].extract_location(dst_src_information)
        fqdn_information = enrichers["name_resolve_enricher"].extract_fqdn(dst_src_information)
        cipher_suite_information = enrichers["cipher_suite_enricher"].get_cipher_suite(packet)
        tls_ssl_version = enrichers["tls_ssl_version_enricher"].get_tls_ssl_version(packet)
        ip_type_information = enrichers["ip_type_enricher"].extract_ip_types(dst_src_information)
        stream_id = enrichers["stream_enricher"].get_stream_id(packet)
        dns_lookup_information = enrichers["dns_lookup_enricher"].detect_dns_request(packet, stream_id)
        ad_value = enrichers["ad_enricher"].test_urls(dns_lookup_information)
        line = CombineHelper.combine_fields(
            [joined_default_cells, location_information, fqdn_information, cipher_suite_information,
             tls_ssl_version, ip_type_information, stream_id, ad_value, dns_lookup_information])
        return line

    @staticmethod
    def combine_fields(fields, quotes_needed=False):
        if quotes_needed:
            return CombineHelper.delimiter.join('"{}"'.format(field) for field in fields)

        return CombineHelper.delimiter.join("{}".format(field) for field in fields)

    @staticmethod
    def join_default_cells(packet, field_names):
        return CombineHelper.delimiter.join('"{}"'.format(packet[field_name]) for field_name in field_names)
