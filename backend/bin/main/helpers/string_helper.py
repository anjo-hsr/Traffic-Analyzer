def remove_quotations(string_value) -> str:
    return string_value.replace("'", "").replace('"', "")


def enclose_with_quotes(string_value) -> str:
    return '"{}"'.format(string_value)
