from typing import Dict, TYPE_CHECKING, List

if TYPE_CHECKING:
    from main.enrichers.enricher import Enricher


class PrintHelper(object):
    @staticmethod
    def print_dict(dict_variable: Dict[str, str], text_with_placeholder: str) -> None:
        print(text_with_placeholder.format(len(dict_variable)))
        for key in dict_variable:
            print("{} --> {}".format(key, dict_variable[key]))

        print("\n\n")

    @staticmethod
    def print_list(list_variable: List[str], text_with_placeholder: str) -> None:
        print(text_with_placeholder.format(len(list_variable)))
        print_list = ", ".join(key for key in list_variable)
        print(print_list)
        print("\n\n")

    @staticmethod
    def print_enrichers(enrichers: Dict[str, "Enricher"]) -> None:
        for enricher_key in enrichers:
            enrichers[enricher_key].print()

    @staticmethod
    def print_error(error_text: str) -> None:
        banner = "#" * 120
        general_text = "An error occured:"
        print_elements = [banner, general_text, error_text, banner]

        print("\n".join(element for element in print_elements))

    @staticmethod
    def print_nothing(enricher_type: str) -> None:
        print("Nothing to print for {}.".format(enricher_type))
