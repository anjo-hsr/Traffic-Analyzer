import re
from os import path, remove

from main.combiners.field_combiner import FieldCombiner
from main.enricher_jar import EnricherJar
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_move_helper, file_name_helper, file_read_helper, file_write_helper, \
    file_path_helper
from main.helpers.file.file_name_helper import get_new_filename
from main.helpers.print_helper import PrintHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


def enrich_file(dirpath, file, new_file, enricher_jar) -> None:
    with \
            open(path.join(dirpath, file), encoding="utf-8") as capture, \
            open(path.join(dirpath, new_file), "w", encoding="utf-8") as output_file:
        csv_reader = file_read_helper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, enricher_jar, output_file)


def loop_through_lines(csv_reader, enricher_jar, output_file) -> None:
    for index, packet in enumerate(csv_reader):
        if file_read_helper.is_header(index):
            default_header = csv_reader.fieldnames
            enricher_classes = enricher_jar.enricher_classes
            helper_headers = [enricher_classes[helper_key].header for helper_key in enricher_classes]
            line = FieldCombiner.join_list_elements(default_header + helper_headers, False)
            line = fix_thsark_fields(line)
            set_enricher_headers(enricher_jar, helper_headers)

        else:
            information_dict = enricher_jar.get_information_dict(packet)
            joined_default_cells = FieldCombiner.join_default_cells(packet, csv_reader.fieldnames)
            enriched_line = FieldCombiner.delimiter.join(
                str(information_dict.get(key, "")) for key in enricher_jar.enricher_headers)
            line = FieldCombiner.combine_packet_information(joined_default_cells, enriched_line)

        file_write_helper.write_line(output_file, line)


def fix_thsark_fields(line) -> str:
    # Delete this line if debian has deployed wireshark v3.x In wireshark / tshark v2.x ssl is the search key for
    # encrypted and bootp is the search key for dhcp traffic. ssl.* and bootp.* could be deprecated in future releases
    # https://tracker.debian.org/pkg/wireshark
    # https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html
    search_replace_touples = [
        (r"ssl\.", r"tls."),
        (r"bootp\.", r"dhcp.")
    ]
    return substitute_line(line, search_replace_touples)


def substitute_line(line, search_replace_touples) -> str:
    for touple in search_replace_touples:
        line = re.sub(touple[0], touple[1], line)
    return line


def set_enricher_headers(enricher_jar, helper_headers) -> None:
    enricher_headers = []
    for header in helper_headers:
        enricher_headers = enricher_headers + header.split(",")

    enricher_jar.enricher_headers = enricher_headers


def main() -> None:
    run(EnvironmentHelper().get_environment())


def run(environment_variables, print_enrichers=False) -> None:
    csv_tmp_path = environment_variables["csv_tmp_path"]
    csv_capture_path = environment_variables["csv_capture_path"]
    limiter = TrafficLimitHelper(3, 1)
    enricher_jar = EnricherJar(limiter)

    for file_path in file_path_helper.get_file_paths(csv_tmp_path, file_name_helper.is_normal_csv_file):
        original_filename = file_path["filename"]
        temp_filename = get_new_filename(original_filename, "csv", "", "-enriched")
        enrich_file(file_path["path"], file_path["filename"], temp_filename, enricher_jar)
        remove(path.join(file_path["path"], file_path["filename"]))

        is_production_environment = environment_variables["environment"] == "production"
        new_file_name = original_filename if is_production_environment else temp_filename
        file_move_helper.move_file(
            path.join(file_path["path"], temp_filename),
            path.join(csv_capture_path, new_file_name)
        )

    if print_enrichers:
        PrintHelper.print_enrichers(enricher_jar.enricher_classes)


if __name__ == "__main__":
    main()
