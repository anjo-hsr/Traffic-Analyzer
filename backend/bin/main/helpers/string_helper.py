def remove_quotations(string_value) -> str:
    return string_value.replace("'", "").replace('"', "")


def enclose_with_quotes(string_value) -> str:
    return '"{}"'.format(string_value)


def remove_spaces(string_value) -> str:
    return string_value.replace(" ", "")


def get_mac_address_line(mac_address, organization, locally=False) -> str:
    from main.combiners.field_combiner import FieldCombiner

    line = mac_address + FieldCombiner.delimiter
    if locally:
        line += enclose_with_quotes(organization)
    else:
        line += enclose_with_quotes("Locally administered - " + organization)

    return line
