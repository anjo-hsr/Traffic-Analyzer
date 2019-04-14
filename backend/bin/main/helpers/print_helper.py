class PrintHelper:
    @staticmethod
    def print_dict(dict_variable, text_with_placeholder):
        print(text_with_placeholder.format(len(dict_variable)))
        for key in dict_variable:
            print("{} --> {}".format(key, dict_variable[key]))

        print("\n\n")

    @staticmethod
    def print_list(list_variable, text_with_placeholder):
        print(text_with_placeholder.format(len(list_variable)))
        print_list = ", ".join(key for key in list_variable)
        print(print_list)
        print("\n\n")

    @staticmethod
    def print_enrichers(enrichers):
        for enricher_key in enrichers:
            enrichers[enricher_key].print()

    @staticmethod
    def print_error(error_text):
        banner = "#" * 120
        general_text = "An error occured:"
        print_elements = [banner, general_text, error_text, banner]

        print("\n".join(element for element in print_elements))
