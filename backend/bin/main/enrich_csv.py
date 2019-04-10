import re

from os import path, walk, remove

import main.helpers.file_helper as file_helper

from main.helpers.environment_helper import EnvironmentHelper
from main.enrichers.location_enricher import LocationEnricher
from main.enrichers.name_resolve_enricher import NameResolverEnricher
from main.helpers.combine_helper import CombineHelper
from main.enrichers.cipher_suite_enricher import CipherSuiteEnricher
from main.enrichers.tls_enricher import TlsEnricher


def loop_through_lines(csv_reader, helpers, output_file):
    for index, packet in enumerate(csv_reader):
        if file_helper.is_header(index):
            default_header = csv_reader.fieldnames
            helper_headers = [helpers[helper_key].header for helper_key in helpers]
            line = CombineHelper.combine_fields(default_header + helper_headers, False)

        else:
            joined_default_cells = CombineHelper.join_default_cells(packet)
            line = CombineHelper.combine_packet_information(joined_default_cells, helpers, packet)

        file_helper.write_line(output_file, line)


def print_dicts(helpers):
    for helper_key in helpers:
        helpers[helper_key].print()


def create_helpers():
    return {
        "locator": LocationEnricher(),
        "name_resolver": NameResolverEnricher(),
        "cipher_suites": CipherSuiteEnricher(),
        "tls_ssl_version": TlsEnricher()
    }


def main():
    run(EnvironmentHelper.get_environment())


def run(environment_variables):
    csv_path = environment_variables["csv_path"]
    csv_enriched_path = environment_variables["csv_enriched_path"]

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            helpers = create_helpers()

            if file_helper.is_normal_csv_file(file):
                new_file = re.sub(".csv$", "-enriched.csv", str(file))
                enrich_file(dirpath, file, helpers, new_file)
                remove(path.join(dirpath, file))

    for (dirpath, dirnames, filenames) in walk(csv_path):
        for file in filenames:
            if file_helper.is_enriched_csv_file(file):
                file_helper.move_file(
                    path.join(dirpath, file),
                    path.join(csv_enriched_path, file)
                )


def enrich_file(dirpath, file, helpers, new_file):
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_reader = file_helper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, helpers, output_file)

        print_dicts(helpers)


if __name__ == "__main__":
    main()
