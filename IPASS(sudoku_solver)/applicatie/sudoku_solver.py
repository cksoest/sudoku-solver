import random


class Sudoku:

    """
    You can use this class for creating a sudoku-objects from a string
    or from a file. With the method "solve" you can solve any sudoku.
    """

    gamble_list = []
    tabu_list = []
    gamble_counter = 0
    loop_counter = 0
    fault_counter = 0
    gamble_depht = 0

    def __init__(self, sudoku):
        """
        This constructor create an object of the given sudoku.
        The constructor converts the given string in a 2d list
        that contains 9 sub-lists that performs the rows of the sudoku.
        For the known values you can use the numbers 1 to 9, and for the
        unknown values you can use any other character or a zero.
        The sign for the unknown values is "-", and for the known values
        the number it self. This data will be stored in attribute "data"
        of the created object.
        :param sudoku: A string with a length of 81 characters.
        """
        if len(sudoku) != 81:
            raise IndexError("The length of the given sudoku must be 81 characters, the given sudoku has a "
                             "length of " + str(len(sudoku)) + " characters")
        self.data = []
        known_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        char_counter = 0
        row = []
        for char in sudoku:
            char_counter = char_counter + 1
            if char in known_values:
                row.append(int(char))
            else:
                row.append("-")
            if char_counter == 9:
                self.data.append(row)
                char_counter = 0
                row = []

    @classmethod
    def from_file(cls, file_name):
        """
        This method returns the stored sudoku from the given file,
        and create from that data a sudoku-object.
        :param file_name: location where the file is stored.
        :return: A sudoku-object with the sudoku from the file.
        """
        sudoku = ""
        try:
            with open(file_name + ".txt", "r") as file:
                for line in file:
                    for num in line:
                        if num == "\n":
                            pass
                        else:
                            sudoku = sudoku + num
        except FileNotFoundError:
            raise FileNotFoundError("The file \"" + file_name + ".txt\" cannot be found.")
        if len(sudoku) != 81:
            raise IndexError("The length of the sudoku in the file must be 81 characters, the sudoku "
                             "in the file" + file_name + " .txt has a length of " + str(len(sudoku)) + " characters")
        return cls(sudoku)

    def get_data(self):
        """
        This method returns the data of the sudoku-object.
        :return: A 2d list sudoku.
        """
        return self.data

    def set_data(self, data):
        """
        This method sets the attribute "data" of the object the given data.
        :param data: A 2d list sudoku
        """
        self.data = data

    @staticmethod
    def get_colomns(sudoku):
        """
        This method separates the colomns of the given sudoku
        in a 2d list. And returns this list.
        :param sudoku: A 2d list sudoku.
        :return: The colomns of the sudoku in a 2d list.
        """
        colomns = []
        for i in range(9):
            colomn = []
            for row in sudoku:
                colomn.append(row[i])
            colomns.append(colomn)
        return colomns

    @staticmethod
    def get_subgrids(sudoku):
        """
        This method separates the subgrids of the given sudoku
        in a 2d list. And returns this list.
        :param sudoku:  A 2d list sudoku.
        :return:  The subgrids of the sudoku in a 2d list.
        """
        subgrids = []
        index_values = {
            0: [0, 3, 0, 3], 1: [0, 3, 3, 6], 2: [0, 3, 6, 9], 3: [3, 6, 0, 3], 4: [3, 6, 3, 6], 5: [3, 6, 6, 9],
            6: [6, 9, 0, 3], 7: [6, 9, 3, 6], 8: [6, 9, 6, 9]}
        for i in range(9):
            subgrid = []
            index = index_values[i]
            rows = sudoku[index[0]:index[1]]
            for row in rows:
                sub_row = row[index[2]:index[3]]
                for num in sub_row:
                    subgrid.append(num)
            subgrids.append(subgrid)
        return subgrids

    @staticmethod
    def set_colomns(colomns):
        """
        This method returns the given colomns of a sudoku, in a sudoku format.
        :param colomns: The colomns of a sudoku in a 2d list.
        :return: A 2d list sudoku.
        """
        sudoku = []
        for i in range(9):
            row = []
            for colomn in colomns:
                row.append(colomn[i])
            sudoku.append(row)
        return sudoku

    @staticmethod
    def set_subgrids(subgrids):
        """
        This method returns the given subgrids of a sudoku, in a sudoku format.
        :param subgrids: The subgrids of the sudoku in a 2d list.
        :return: A 2d list sudoku.
        """
        sudoku = []
        index_values = {
            0: [0, 3, 0, 3], 1: [0, 3, 3, 6], 2: [0, 3, 6, 9], 3: [3, 6, 0, 3], 4: [3, 6, 3, 6], 5: [3, 6, 6, 9],
            6: [6, 9, 0, 3], 7: [6, 9, 3, 6], 8: [6, 9, 6, 9]}
        for i in range(9):
            new_row = []
            index = index_values[i]
            rows = subgrids[index[0]:index[1]]
            for row in rows:
                sub_row = row[index[2]:index[3]]
                for num in sub_row:
                    new_row.append(num)
            sudoku.append(new_row)
        return sudoku

    def create_possibility(self):
        """
        This method makes a list with the numbers 1, 2, 3, 5, 5, 6, 7, 8 and 9
        of all the unknown values. in the attribute "data" of the object
        """
        new_data = []
        new_row = []
        for row in self.data:
            num_counter = 0
            for num in row:
                num_counter = num_counter + 1
                if type(num) == int:
                    new_row.append(num)
                else:
                    new_row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
                if num_counter == 9:
                    new_data.append(new_row)
                    num_counter = 0
                    new_row = []
        self.data = new_data

    @staticmethod
    def alldifferent(data):
        """
        This method checks each list of the given 2d list for the next thing:
        The known values may not exists in the lists of the possibility for the unknown values.
        So this method remove all known values from that lists. And returns the filtered data.
        :param data: A 2d list.
        :return: A filtered data 2d list, filtered by this method.
        """
        new_data = []
        for row in data:
            new_row = []
            int_dict = {}
            choices_dict = {}
            pos_index = -1
            for pos in row:
                pos_index = pos_index + 1
                if type(pos) == int:
                    int_dict[pos_index] = pos
                elif type(pos) == list:
                    choices_dict[pos_index] = pos
            for num in int_dict:
                for choices in choices_dict:
                    new_choices = []
                    choice_index = -1
                    for choice in choices_dict[choices]:
                        choice_index = choice_index + 1
                        if int_dict[num] != choice:
                            new_choices.append(choices_dict[choices][choice_index])
                    choices_dict[choices] = new_choices
            for num in int_dict:
                new_row.insert(num, int_dict[num])
            for choice in choices_dict:
                new_row.insert(choice, choices_dict[choice])
            new_data.append(new_row)
        return new_data

    @staticmethod
    def alldifferent_rcs(sudoku):
        """
        This method runs the method "alldifferent" on  the
        rows, colomns and subgrids of the given sudoku. And returns the filtered sudoku.
        :param sudoku: A 2d list sudoku.
        :return: A 2d list sudoku, filtered by the method "alldifferent".
        """
        sudoku = Sudoku.alldifferent(sudoku)
        colomns = Sudoku.get_colomns(sudoku)
        colomns_ad = Sudoku.alldifferent(colomns)
        sudoku = Sudoku.set_colomns(colomns_ad)
        subgrids = Sudoku.get_subgrids(sudoku)
        subgrids_ad = Sudoku.alldifferent(subgrids)
        sudoku = Sudoku.set_subgrids(subgrids_ad)
        return sudoku

    @staticmethod
    def one_check(sudoku):
        """
        This method checks each position of the sudoku for the next thing:
        If there is a position that contains one possibility.
        Then that will be the value of that position.
        And returns the filtered sudoku.
        :param sudoku: A 2d list sudoku.
        :return: A 2d list sudoku, that is check by this method.
        """
        row_index = -1
        for row in sudoku:
            row_index = row_index + 1
            num_index = -1
            for num in row:
                num_index = num_index + 1
                if type(num) == list:
                    if len(num) == 1:
                        sudoku[row_index][num_index] = num[0]
        return sudoku

    @staticmethod
    def one_possibility(data):
        """
        This method check each list of the given 2d list for the next thing:
        If there is a number in te lists of the possibilities for the unknown values
        that exists once. Then that position will be value of number that exist once.
        And returns the filtered data.
        :param data: A 2d list.
        :return: A 2d list, filtered by this method.
        """
        for i in range(9):
            to_check = []
            once_num = []
            for pos in data[i]:
                if type(pos) == list:
                    for num in pos:
                        to_check.append(num)
            for j in range(1, 10):
                counted = to_check.count(j)
                if counted == 1:
                    once_num.append(j)
            if len(once_num) > 0:
                pos_index = -1
                for pos in data[i]:
                    pos_index = pos_index + 1
                    if type(pos) == list:
                        for num in once_num:
                            if num in pos:
                                data[i][pos_index] = num
        return data

    @staticmethod
    def one_possibility_c(sudoku):
        """
        This method checks the colomns of the given sudoku with the method "one_possibility".
        And returns the sudoku.
        :param sudoku: 2d list sudoku.
        :return: A 2d list sudoku, where the colomns are checked by the method "one_possibility".
        """
        colomns = Sudoku.get_colomns(sudoku)
        colomns_op = Sudoku.one_possibility(colomns)
        sudoku = Sudoku.set_colomns(colomns_op)
        return sudoku

    @staticmethod
    def one_possibility_s(sudoku):
        """
        This method checks the subgrids of the given sudoku with the method "one_possibility".
        And returns the sudoku.
        :param sudoku: 2d list sudoku.
        :return: A 2d list sudoku, where the subgrids are checked by the method "one_possibility".
        """
        subgrids = Sudoku.get_subgrids(sudoku)
        subgrids_op = Sudoku.one_possibility(subgrids)
        sudoku = Sudoku.set_subgrids(subgrids_op)
        return sudoku

    @staticmethod
    def alldifferent_strategy(sudoku):
        """
        This method runs the standard check over the sudoku. And returns the sudoku.
        :param sudoku: A 2d list sudoku.
        :return: A 2d list sudoku checked by this method.
        """
        sudoku = Sudoku.alldifferent_rcs(sudoku)
        sudoku = Sudoku.one_check(sudoku)
        sudoku = Sudoku.alldifferent_rcs(sudoku)
        sudoku = Sudoku.one_possibility(sudoku)
        sudoku = Sudoku.alldifferent_rcs(sudoku)
        sudoku = Sudoku.one_possibility_c(sudoku)
        sudoku = Sudoku.alldifferent_rcs(sudoku)
        sudoku = Sudoku.one_possibility_s(sudoku)
        return sudoku

    @staticmethod
    def double_check(data):
        """
        This metod checks each list in the given 2d list for double values.
        And returns a True or a False.
        :param data: A 2d list.
        :return: True or False.
        """
        for row in data:
            for num0 in row:
                if type(num0) == int:
                    check = num0
                    num_counter = 0
                    for num1 in row:
                        if type(num1) == int:
                            if num1 == check:
                                num_counter = num_counter + 1
                    if num_counter > 1:
                        return True
        return False

    @staticmethod
    def double_check_rcs(sudoku):
        """
        This method checks for double values for the rows, colomns
        and subgrids of the given sudoku.
        :param sudoku: A 2d list sudoku.
        :return: True or False.
        """
        colomns = Sudoku.get_colomns(sudoku)
        subgrids = Sudoku.get_subgrids(sudoku)
        if Sudoku.double_check(sudoku) or Sudoku.double_check(colomns) or Sudoku.double_check(subgrids):
            return True
        else:
            return False

    @staticmethod
    def zero_check(sudoku):
        """
        This method check that the given sudoku has
        a list with a length of zero. And returns a True aor a False.
        :param sudoku: A 2d list sudoku.
        :return: True or False
        """
        for row in sudoku:
            for num in row:
                if type(num) == list:
                    if len(num) == 0:
                        return True
        return False

    @staticmethod
    def count_known_values(sudoku):
        """
        This method counts all known values in the given sudoku.
        And returns the number of known values.
        :param sudoku: a 2d list sudoku.
        :return: number of known values.
        """
        counter = 0
        for row in sudoku:
            for num in row:
                if type(num) == int:
                    counter = counter + 1
        return counter

    @staticmethod
    def get_min_choice(sudoku):
        """
        This method gets the index of the best gamble position you can made.
        The method get first position with the fewest possibilities. And returns this index.
        :param sudoku: A 2d list sudoku.
        :return: The index of the best gamble position.
        """
        min_len = 2
        while True:
            row_index = -1
            for row in sudoku:
                row_index = row_index + 1
                num_index = -1
                for num in row:
                    num_index = num_index + 1
                    if type(num) == list:
                        if len(num) == min_len:
                            return [row_index, num_index]
            min_len = min_len + 1

    def not_in_tabu_list(self, best_gamble_index, best_gamble_values):
        """
        This method check if the combination of the "best_gamble_index" with "best_gamble_values"
        already exist in the tabu list. And returns a True or a False, with the gamble you can made.
        :param best_gamble_index: The index of the best place, to make a gamble.
        :param best_gamble_values: The values of the "best_gamble_index" position.
        :return: True or False, Gamble that you can made.
        """
        for i in range(len(best_gamble_values)):
            gamble = [best_gamble_index[0], best_gamble_index[1], best_gamble_values[i]]
            if gamble not in self.tabu_list:
                return True, gamble
        return False, None

    def alldifferent_tabu_search(self):
        """
        This method is the algorithm for solving the sudoku.
        Where you fist must run the method "create_possibilities"
        before you can run this method. And the attribute "data"
        of the object will be replaced for the solved sudoku.

        The algorithm works as follows. First there will be check how many known values there are.
        The next step run the alldifferent algorithm and the sudoku strategies. After this
        there is a second known value check. If there is no difference between the two checks.
        Then the tabu search algorithm will make a gamble in the sudoku. And the algorithm will go on.
        When the algorithm detects a fault. The sudoku will be reset, and the gamble that was made
        will be added to the tabu list. The tabu list is a list with all the wrong gambles,
        Now the algorithm knows which gamble not to make again. This all runs in a loop until
        all the values are known.
        """
        new_sudoku = self.data
        while self.count_known_values(new_sudoku) != 81:
            self.loop_counter = self.loop_counter + 1
            known_values_1 = self.count_known_values(new_sudoku)
            new_sudoku = self.alldifferent_strategy(new_sudoku)
            known_values_2 = self.count_known_values(new_sudoku)
            if self.zero_check(new_sudoku) or self.double_check_rcs(new_sudoku):
                if self.gamble_depht == 0:
                    raise IndexError("There is no solution for this sudoku")
                self.gamble_depht = self.gamble_depht - 1
                self.fault_counter = self.fault_counter + 1
                self.tabu_list.append(self.gamble_list[-1])
                del self.gamble_list[-1]
                new_sudoku = self.data
                self.gamble_list = []
                self.gamble_depht = 0
            if known_values_1 == known_values_2:
                best_gamble_index = self.get_min_choice(new_sudoku)
                best_gamble_values = new_sudoku[best_gamble_index[0]][best_gamble_index[1]]
                if len(self.tabu_list) == 0:
                    self.gamble_counter = self.gamble_counter + 1
                    self.gamble_depht = self.gamble_depht + 1
                    self.gamble_list.append([best_gamble_index[0], best_gamble_index[1], best_gamble_values[0]])
                    new_sudoku[best_gamble_index[0]][best_gamble_index[1]] = best_gamble_values[0]
                else:
                    not_in_tabu_list, gamble = self.not_in_tabu_list(best_gamble_index, best_gamble_values)
                    if not_in_tabu_list:
                        self.gamble_counter = self.gamble_counter + 1
                        self.gamble_depht = self.gamble_depht + 1
                        self.gamble_list.append(gamble)
                        new_sudoku[gamble[0]][gamble[1]] = gamble[2]
                    if not not_in_tabu_list:
                        if self.gamble_depht == 0:
                            raise IndexError("There is no solution for this sudoku")
                        self.fault_counter = self.fault_counter + 1
                        self.gamble_depht = self.gamble_depht - 1
                        del self.tabu_list[-len(best_gamble_values):]
                        self.tabu_list.append(self.gamble_list[-1])
                        del self.gamble_list[-1]
                        new_sudoku = self.data
                        self.gamble_list = []
                        self.gamble_depht = 0

        self.data = new_sudoku

    def solve(self):
        """
        This method solves the sudoku. And replace the attribute "data" for the solution.
        """
        self.create_possibility()
        self.alldifferent_tabu_search()

    def print(self):
        """
        This method prints the sudoku in a clean format to the screen.
        """
        if type(self.data) == str:
            print(self.data)
        else:
            row_counter = 0
            print("-------------------------")
            for row in self.data:
                row_counter = row_counter + 1
                print("|", row[0], row[1], row[2], "|", row[3], row[4], row[5], "|", row[6], row[7], row[8], "|")
                if row_counter == 3:
                    print("-------------------------")
                    row_counter = 0

    @staticmethod
    def get_hint(unsolved, solved):
        """
        This method returns a sudoku with a random hint in a 2d list format.
        The hint will be made for the unsolved sudoku.
        :param unsolved: A 2d list unsolved sudoku
        :param solved: A 2d list solution of the unsolved parameter
        :return: solved: A 2d list sudoku with a hint.
        """
        unknown_values = 81 - Sudoku.count_known_values(unsolved)
        if unknown_values == 0:
            raise ValueError("There are no more hints available")
        else:
            hint_pos = random.randrange(unknown_values)
            unknown_value_counter = -1
            row_index = -1
            for row in unsolved:
                row_index = row_index + 1
                num_index = -1
                for num in row:
                    num_index = num_index + 1
                    if type(num) != int:
                        unknown_value_counter = unknown_value_counter + 1
                        if unknown_value_counter == hint_pos:
                            hint = solved[row_index][num_index]
                            unsolved[row_index][num_index] = hint
                            return unsolved
