import re
from collections import OrderedDict

from os import path, walk, remove

import main.helpers.file_helper as file_helper

from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.enrichers.protocol_enricher import ProtocolEnricher
from main.enrichers.tls_enricher import TlsEnricher
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.combine_helper import CombineHelper
from main.helpers.print_helper import PrintHelper


def loop_through_lines(csv_reader, enrichers, output_file):
    for index, packet in enumerate(csv_reader):
        if file_helper.is_header(index):
            default_header = csv_reader.fieldnames
            helper_headers = [enrichers[helper_key].header for helper_key in enrichers]
            line = CombineHelper.combine_fields(default_header + helper_headers, False)

            # Delete this line if debian has deployed wireshark v3.x In wireshark / tshark v2.x ssl is the search key
            # for encrypted traffic. ssl.* could be deprecated in future releases
            # https://packages.qa.debian.org/w/wireshark.html
            # https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html
            line = re.sub(r"ssl.", r"tls.", line)

        else:
            joined_default_cells = CombineHelper.join_default_cells(packet, csv_reader.fieldnames)
            line = CombineHelper.combine_packet_information(joined_default_cells, enrichers, packet)

        file_helper.write_line(output_file, line)


def create_enrichers():
    return OrderedDict([
        ("location_enricher", LocationEnricher()),
        ("name_resolve_enricher", NameResolverEnricher()),
        ("cipher_suite_enricher", CipherSuiteEnricher()),
        ("tls_ssl_version_enricher", TlsEnricher()),
        ("protocol_enricher", ProtocolEnricher())
    ])


def main():
    environment_helper = EnvironmentHelper()
    run(environment_helper.get_environment())


def run(environment_variables):
    csv_tmp_path = environment_variables["csv_tmp_path"]
    csv_capture_path = environment_variables["csv_capture_path"]

    for dirpath, _, filenames in walk(csv_tmp_path):
        for file in filenames:
            enrichers = create_enrichers()

            if file_helper.is_normal_csv_file(file):
                new_file = re.sub(".csv$", "-enriched.csv", str(file))
                enrich_file(dirpath, file, enrichers, new_file)
                remove(path.join(dirpath, file))

    for dirpath, _, filenames in walk(csv_tmp_path):
        for file in filenames:
            if file_helper.is_enriched_csv_file(file):
                file_helper.move_file(
                    path.join(dirpath, file),
                    path.join(csv_capture_path, file)
                )


def enrich_file(dirpath, file, enrichers, new_file):
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_reader = file_helper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, enrichers, output_file)

        PrintHelper.print_enrichers(enrichers)


if __name__ == "__main__":
    main()
