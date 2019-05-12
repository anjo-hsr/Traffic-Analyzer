import re
from os import path, remove

from main.enricher_jar import EnricherJar
from main.helpers.combine_helper import CombineHelper
from main.helpers.environment_helper import EnvironmentHelper
from main.helpers.file import file_move_helper, file_name_helper, file_read_helper, file_write_helper, \
    file_path_helper
from main.helpers.print_helper import PrintHelper
from main.helpers.traffic_limit_helper import TrafficLimitHelper


def enrich_file(dirpath, file, enricher_jar, new_file) -> None:
    with \
            open(path.join(dirpath, file), mode="r", encoding='utf-8') as capture, \
            open(path.join(dirpath, new_file), 'w', encoding='utf-8') as output_file:
        csv_reader = file_read_helper.get_csv_dict_reader(capture)

        loop_through_lines(csv_reader, enricher_jar, output_file)


def loop_through_lines(csv_reader, enricher_jar, output_file) -> None:
    for index, packet in enumerate(csv_reader):
        ip_enumerate_character = ","
        packet["ip.dst"] = packet["ip.dst"].split(ip_enumerate_character)[0]
        packet["ip.src"] = packet["ip.src"].split(ip_enumerate_character)[0]

        if file_read_helper.is_header(index):
            default_header = csv_reader.fieldnames
            enricher_classes = enricher_jar.enricher_classes
            helper_headers = [enricher_classes[helper_key].header for helper_key in enricher_classes]
            line = CombineHelper.combine_fields(default_header + helper_headers, False)

            # Delete this line if debian has deployed wireshark v3.x In wireshark / tshark v2.x ssl is the search key
            # for encrypted traffic. ssl.* could be deprecated in future releases
            # https://tracker.debian.org/pkg/wireshark
            # https://www.wireshark.org/docs/relnotes/wireshark-3.0.0.html
            line = re.sub(r"ssl\.", r"tls.", line)

        else:
            joined_default_cells = CombineHelper.join_default_cells(packet, csv_reader.fieldnames)
            line = CombineHelper.combine_packet_information(joined_default_cells, enricher_jar, packet)

        file_write_helper.write_line(output_file, line)


def main() -> None:
    run(EnvironmentHelper().get_environment())


def run(environment_variables, print_enrichers=False) -> None:
    csv_tmp_path = environment_variables["csv_tmp_path"]
    csv_capture_path = environment_variables["csv_capture_path"]
    limiter = TrafficLimitHelper(3, 1)
    enricher_jar = EnricherJar(limiter)

    for file_path in file_path_helper.get_file_paths(csv_tmp_path, file_name_helper.is_normal_csv_file):
        new_file = re.sub(".csv$", "-enriched.csv", str(file_path["filename"]))
        enrich_file(file_path["path"], file_path["filename"], enricher_jar, new_file)
        remove(path.join(file_path["path"], file_path["filename"]))

    if print_enrichers:
        PrintHelper.print_enrichers(enricher_jar.enricher_classes)

    for file_path in file_path_helper.get_file_paths(csv_tmp_path, file_name_helper.is_enriched_csv_file):
        file_move_helper.move_file(
            path.join(file_path["path"], file_path["filename"]),
            path.join(csv_capture_path, file_path["filename"])
        )


if __name__ == "__main__":
    main()
