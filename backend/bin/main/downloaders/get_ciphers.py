from os import path

from main.helpers.Combiner import Combiner
import main.helpers.FileHelper as FileHelper


def calculate_hex(hex_pair):
    hex_list = hex_pair.split(",")
    first_value = int(hex_list[0], 16) * pow(16, 2)
    second_value = int(hex_list[1], 16)
    return first_value + second_value


def combine_information(row):
    cipher_suite_number = calculate_hex(row["Value"])
    description = row["Description"]
    recommended = row["Recommended"]
    line = Combiner.combine_fields([cipher_suite_number, description, recommended])
    return line


def write_row(output_file, row):
    try:
        line = combine_information(row)
        FileHelper.write_line(output_file, line)
    except ValueError:
        pass


def main():
    url = "https://www.iana.org/assignments/tls-parameters/tls-parameters-4.csv"
    filename = FileHelper.download_file(url)
    destination_file = path.join("..", "..", "files", "cipher_suites.csv")

    with \
            open(filename, mode="r", encoding='utf-8') as csv_file, \
            open(destination_file, mode='w', encoding='utf-8') as output_file:
        csv_reader = FileHelper.get_csv_dict_reader(csv_file)

        header = "cipher_suite_number,description,recommended"
        FileHelper.write_line(output_file, header)

        for row in csv_reader:
            write_row(output_file, row)

    FileHelper.remove_file(filename)


if __name__ == "__main__":
    main()
