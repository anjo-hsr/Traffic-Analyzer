class PrintHelper:
    @staticmethod
    def print_dict(dict_variable, text_with_placeholder):
        print(text_with_placeholder.format(len(dict_variable)))
        for key in dict_variable:
            print("{} --> {}".format(key, dict_variable[key]))

        print("\n\n")
