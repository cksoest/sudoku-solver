import sudoku_solver


def get_language():
    """
    This function returns the language, which is set in the "data/languages/language.txt" file
    :return: The language, which is set.
    """
    with open("data/languages/language.txt", "r") as file:
        for line in file:
            return line


def set_language(language):
    """
    This function sets the language to the given language in the "data/languages/language.txt" file.
    :param language: language you want to use.
    """
    with open("data/languages/language.txt", "w") as file:
        file.write(language)


def get_text(language):
    """
    This function returns the dataset of the right language
    To the application. In a 2d list format.
    :param language: language which is set for the application.
    :return: dataset for the application.
    """
    text = []
    with open("data/languages/" + language + ".txt", "r") as file:
        for line in file:
            text.append(line[:-1])
    return text


def get_manual():
    """
    This function returns the manuals to the application.
    :return: manual
    """
    language = get_language()
    manual = ""
    with open("data/manuals/" + language + "-Manual.txt", "r") as file:
        for line in file:
            manual = manual + line
    return manual


def main_menu():
    """
    This is the main menu with all the available options.
    """
    language = get_language()
    text = get_text(language)
    choice = ""
    possible_choices = ["1", "2", "3", "4"]
    while choice not in possible_choices:
        print("----------------------------------------------------")
        print(text[0] + "\n" + text[1] + "\n" + text[2] + "\n" + text[3])
        choice = input(text[7])
        if choice not in possible_choices:
            print(text[15])
            main_menu()
    if choice == "1":
        sudoku_menu(text, False)
    elif choice == "2":
        sudoku_menu(text, True)
    elif choice == "3":
        change_language_option(text)
    elif choice == "4":
        manual_option(text)


def sudoku_menu(text, hint):
    """
    This is menu for the "Solve sudoku" an "Hint for a sudoku" option.
    Where you can choose for text import of file import.
    :param text: text needed for the application.
    :param hint: Choice if you want a hint or not.
    """
    choice = ""
    possible_choices = ["1", "2", "x"]
    while choice not in possible_choices:
        print("----------------------------------------------------")
        print(text[4] + "\n" + text[5] + "\n" + text[6])
        choice = input(text[7])
        if choice not in possible_choices:
            print(text[16])
            sudoku_menu(text, hint)
    if choice == "1":
        sudoku_text_option(text, hint)
    elif choice == "2":
        sudoku_file_option(text, hint)
    elif choice == "x":
        main_menu()


def sudoku_file_option(text, hint):
    """
    This function must be called if you want to open
    a sudoku from a file.
    :param text: text needed for the application.
    :param hint: Choice if you want a hint or not.
    """
    choice = ""
    while choice != "x":
        print("----------------------------------------------------")
        choice = input(text[9])
        if choice == "x":
            break
        else:
            try:
                sudoku = sudoku_solver.Sudoku.from_file("data/sudokus/" + choice)
                print(text[13])
                sudoku.print()
            except FileNotFoundError:
                print(text[18])
            except IndexError:
                print(text[19])
            else:
                if hint:
                    get_hint_option(text, hint, sudoku)
                else:
                    try:
                        sudoku.solve()
                        print(text[14])
                        sudoku.print()
                    except IndexError:
                        print(text[20])

    sudoku_menu(text, hint)


def sudoku_text_option(text, hint):
    """
    This function must be called if you want to open a sudoku
    from a text string.
    :param text: text needed for the application.
    :param hint: Choice if you want a hint or not.
    """
    choice = ""
    while choice != "x":
        print("----------------------------------------------------")
        choice = input(text[8])
        if choice == "x":
            break
        else:
            try:
                sudoku = sudoku_solver.Sudoku(choice)
                print(text[13])
                sudoku.print()
            except IndexError:
                print(text[17])
            else:
                if hint:
                    get_hint_option(text, hint, sudoku)
                else:
                    try:
                        sudoku.solve()
                        print(text[14])
                        sudoku.print()
                    except IndexError:
                        print(text[20])

    sudoku_menu(text, hint)


def manual_option(text):
    """
    This function shows the manual of teh application.
    :param text: text needed for the application.
    """
    print("----------------------------------------------------")
    print(text[10] + "\n")
    print(get_manual())
    choice = input()
    while choice != "x":
        choice = input()
    main_menu()


def change_language_option(text):
    """
    This function give you the option to change the language.
    :param text: text needed for the application.
    """
    choice = ""
    while choice != "NL" or choice != "EN":
        print("----------------------------------------------------")
        print(text[11] + "\n" + text[12])
        choice = input(text[7])
        if choice == "NL" or choice == "EN":
            set_language(choice)
            main_menu()
        elif choice == "x":
            main_menu()
        else:
            print(text[21])


def get_hint_option(text, hint, sudoku):
    """
    This function prints a hint of the given sudoku to the screen.
    :param text: text needed for the application.
    :param hint: Choice if you want a hint or not.
    :param sudoku: A sudoku where you want a hint for.
    """
    unsolved = sudoku.get_data()
    try:
        sudoku.solve()
        solved = sudoku.get_data()
        sudoku.set_data(sudoku_solver.Sudoku.get_hint(unsolved, solved))
        sudoku.print()
    except IndexError:
        print(text[20])
    else:
        choice = ""
        while choice != "1":
            print("----------------------------------------------------")
            print(text[22] + "\n" + text[6])
            choice = input(text[7])
            if choice == "1":
                try:
                    get_hint_option(text, hint, sudoku)
                except ValueError:
                    print(text[23])
            elif choice == "x":
                sudoku_file_option(text, hint)
            else:
                print(text[24])


try:
    main_menu()
except KeyboardInterrupt:
    pass
