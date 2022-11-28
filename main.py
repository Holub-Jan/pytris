class Game:
    def __init__(self, rows_number, cols_number, max_score):

        # Flexible variables for changing the size and length of the game
        self.rows_number = rows_number
        self.cols_number = cols_number
        self.max_score = max_score

        self.field_matrix = list()

        self.available_block_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.column_names = ['q', 'w', 'e', 'r', 't']
        self.score = 0

        self.logic = Logic(self.rows_number, self.cols_number, self.field_matrix, self.available_block_list,
                           self.column_names, self.score, self.get_block_value, self.change_block_value)
        self.ui_manager = UiManager(cols_number, rows_number, self.column_names, self.field_matrix, self.score)
        self.controller = Controller(self.column_names, self.end)

    # Start game loop
    def game_loop(self):
        import os

        # tests below
        self.logic.gen_empty_field()

        while True:
            os.system('cls')
            gen_block = self.logic.gen_rand_block()
            self.ui_manager.next_block = gen_block

            self.ui_manager.display_manager()

            user_input = self.controller.get_user_input()
            placed_block = self.logic.place_block(gen_block, user_input)
            self.logic.update_matrix([placed_block])

    # For changing values of blocks
    def change_block_value(self, pos, value):
        self.field_matrix[pos[0]][pos[1]] = value

    # Return block value based on position
    def get_block_value(self, block):
        return self.field_matrix[block[0]][block[1]]

    # Close program
    @staticmethod
    def end():
        quit()


class UiManager:
    def __init__(self, cols_num, rows_num, col_names, field_matrix, score):
        self.cols_number = cols_num
        self.rows_number = rows_num
        self.column_names = col_names
        self.field_matrix = field_matrix
        self.score = score

        self.next_block = 0
        self.border_num = 2

    # For managing displaying required parts
    def display_manager(self):

        self.display_col_options()
        self.display_field_matrix()

        self.display_score_bar()

    # Displaying column options for better visibility
    def display_col_options(self):
        for col in range(self.cols_number + self.border_num):
            if col not in [0, self.cols_number + (self.border_num / 2)]:
                print(self.column_names[col - 1], end=' ')
            else:
                print(' ', end=' ')
        print()

    # Displaying field matrix with borders
    def display_field_matrix(self):
        for row in range(self.rows_number + self.border_num):
            for col in range(self.cols_number + self.border_num):
                block_value = self.border_display(row, col)
                self.field_display(block_value)
            print()

    # Border logic displaying
    def border_display(self, row, col):
        block_value = -1
        # Displaying borders on left, right and bottom
        if col in [0, self.cols_number + (self.border_num / 2)] or row == self.rows_number + (
                self.border_num / 2):
            print('@', end=' ')
        elif row == 0:
            print(' ', end=' ')
        else:
            block_value = self.field_matrix[row - int(self.border_num / 2)][col - int(self.border_num / 2)]

        return block_value

    # Field logic displaying
    @staticmethod
    def field_display(block_value):
        # Zero value means empty space, so we display nothing
        if block_value != -1:
            if block_value == 0:
                print(' ', end=' ')
            # Displaying the rest of the values
            else:
                print(block_value, end=' ')

    # Display score bar
    def display_score_bar(self):
        print(f'Score: {self.score}')
        print(f'Next piece: {self.next_block}')


class Controller:
    def __init__(self, expected_input, end_opt):
        self.expected_input = expected_input
        self.end_opt = end_opt

    # Getting users choice of column addition
    def get_user_input(self):
        # Saving users initial input
        user_input = input('Choose a column to add the piece: ')

        # Checking if user chose a viable option
        # If not, display available options and ask again until viable option is selected
        while user_input not in self.expected_input:
            if user_input == 'exit':
                self.end_opt()
            else:
                print('\nSelected column is not available\nPlease select one of the following options: ',
                      ', '.join(f'{opt}' for opt in self.expected_input))
                user_input = input('Choose a column to add the piece: ')

        return user_input


class Logic:
    def __init__(self, rows_num, cols_num, field_matrix, block_list, col_names, score, get_block_value,
                 change_block_value):
        self.rows_number = rows_num
        self.cols_number = cols_num
        self.field_matrix = field_matrix
        self.available_block_list = block_list
        self.column_names = col_names
        self.score = score
        self.get_block_value = get_block_value
        self.change_block_value = change_block_value

    # Generating new empty playing field
    def gen_empty_field(self):
        for _ in range(self.rows_number):
            self.field_matrix.append([0 for _ in range(self.cols_number)])

    # Generating a block from available options
    def gen_rand_block(self):
        import random
        rand_block = random.choice(self.available_block_list)

        return rand_block

    # Function for adding to total score
    def add_to_score(self, to_add):
        self.score += to_add

    # Place a block the lowest possible spot in selected column
    def place_block(self, block, column):
        col_num = self.column_names.index(column)

        for col in range(self.cols_number):
            if col == col_num:
                for row in range(self.rows_number):
                    check_pos = self.field_matrix[(self.rows_number - 1) - row][col]
                    if check_pos == 0:
                        self.field_matrix[(self.rows_number - 1) - row][col] = block
                        return (self.rows_number - 1) - row, col

    # Update matrix after choice is made
    def update_matrix(self, blocks_to_check):
        cols_to_update = set()

        for check_block in blocks_to_check:
            block_value = self.get_block_value(check_block)
            linked_blocks = self.connected_blocks(check_block, set())

            if len(linked_blocks) > 2:

                for block in linked_blocks:
                    cols_to_update.add(block[1])
                    self.change_block_value(block, 0)

                self.add_to_score(len(linked_blocks) * block_value)

        for col in cols_to_update:
            self.update_column(col)

    # Adding gravity to column blocks
    def update_column(self, col):
        col_values = [self.field_matrix[row][col] for row in range(self.rows_number)]

        if max(col_values) == 0:
            return

        to_check = list()
        to_pop = [col_values[index] for index in range(len(col_values)) if col_values[index] != 0]

        row_idx = self.rows_number
        for i in reversed(range(len(to_pop))):
            row_idx -= 1
            self.field_matrix[row_idx][col] = to_pop[i]
            to_check.append((row_idx, col))

        for i in range(row_idx):
            self.field_matrix[i][col] = 0

        self.update_matrix(to_check)

    # Get connected set of blocks with same value as origin
    def connected_blocks(self, ori_block, seen):
        seen.add(ori_block)
        next_to = self.get_adjacent_same(ori_block, self.get_block_value(ori_block))

        for pos in next_to:
            if pos not in seen:
                ori_block = pos
                self.connected_blocks(ori_block, seen)

        return seen

    # Getting a list of adjacent same blocks within the field metrix
    def get_adjacent_same(self, block_pos, block_value):
        next_to = set()

        # left
        if block_pos[1] > 0:
            pos = (block_pos[0], block_pos[1] - 1)
            if self.field_matrix[pos[0]][pos[1]] == block_value:
                next_to.add(pos)
        # right
        if block_pos[1] < self.cols_number - 1:
            pos = (block_pos[0], block_pos[1] + 1)
            if self.field_matrix[pos[0]][pos[1]] == block_value:
                next_to.add(pos)
        # up
        if block_pos[0] > 0:
            pos = (block_pos[0] - 1, block_pos[1])
            if self.field_matrix[pos[0]][pos[1]] == block_value:
                next_to.add(pos)
        # down
        if block_pos[0] < self.rows_number - 1:
            pos = (block_pos[0] + 1, block_pos[1])
            if self.field_matrix[pos[0]][pos[1]] == block_value:
                next_to.add(pos)

        return next_to


number_of_rows = 10
number_of_columns = 5
score_to_win = 100

game = Game(number_of_rows, number_of_columns, score_to_win)
game.game_loop()

''' for testing
game.field_matrix = [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 4, 0, 0, 2],
                     [3, 0, 4, 4, 0],
                     [0, 4, 0, 0, 2],
                     [3, 0, 4, 4, 2],]
game.display_field_matrix()
for col in range(number_of_columns):
    game.update_column(col)

game.display_field_matrix()
'''
