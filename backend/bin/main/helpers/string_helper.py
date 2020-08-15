from typing import Union


def remove_quotations(string_value: str) -> str:
    return string_value.replace("'", "").replace('"', "")


def enclose_with_quotes(string_value: Union[str, int]) -> str:
    return '"{}"'.format(string_value)


def remove_spaces(string_value: str) -> str:
    return string_value.replace(" ", "")


def get_mac_address_line(mac_address: str, organization: str, is_locally_administered: bool = False) -> str:
    from main.combiners.field_combiner import FieldCombiner

    line = mac_address + FieldCombiner.delimiter
    if is_locally_administered:
        line += enclose_with_quotes("Locally administered - " + organization)
    else:
        line += enclose_with_quotes(organization)

    return line
