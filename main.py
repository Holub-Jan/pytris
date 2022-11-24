class NewGame:

    def __init__(self, rows_number, cols_number, max_score):

        # Flexible variables for changing the size and length of the game
        self.rows_number = rows_number
        self.cols_number = cols_number
        self.max_score = max_score

        self.field_matrix = list()
        self.score = 0

        self.available_block_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.column_names = ['q', 'w', 'e', 'r', 't']
        # Symmetric number of walls for row and column ( border size * 2 )
        self.border_num = 2

    # Close program
    @staticmethod
    def end():
        quit()

    # Start game loop
    # TODO : currently used for testing, last thing to complete?
    def game_loop(self):

        # tests below
        game.gen_empty_field()

        while True:
            gen_block = self.gen_rand_block()
            self.display_manager(gen_block)
            user_input = self.get_user_input()
            placed_block = self.place_block(gen_block, user_input)
            self.update_matrix(placed_block)

    # Reset game variables
    # TODO : add function for resting the game
    def game_reset(self):
        pass

    # Function for adding to total score
    def add_to_score(self, to_add):
        self.score += to_add

    # For managing displaying required parts
    @staticmethod
    def display_manager(new_block):

        game.display_col_options()
        game.display_field_matrix()

        game.display_score_bar(new_block)

    # Generating new empty playing field
    def gen_empty_field(self):
        for _ in range(self.rows_number):
            self.field_matrix.append([0 for _ in range(self.cols_number)])

    # Generating a block from available options
    def gen_rand_block(self):
        import random
        rand_block = random.choice(self.available_block_list)

        return rand_block

    # Getting users choice of column addition
    def get_user_input(self):
        # Saving users initial input
        user_input = input('Choose a column to add the piece: ')

        # Checking if user chose a viable option
        # If not, display available options and ask again until viable option is selected
        while user_input not in self.column_names:
            if user_input == 'exit':
                self.end()
            else:
                print('\nSelected column is not available\nPlease select one of the following options: ',
                      ', '.join(f'{opt}' for opt in self.column_names))
                user_input = input('Choose a column to add the piece: ')

        return user_input

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
                block_value = -1
                # Displaying borders on left, right and bottom
                if col in [0, self.cols_number + (self.border_num / 2)] or row == self.rows_number + (
                        self.border_num / 2):
                    print('@', end=' ')
                elif row == 0:
                    print(' ', end=' ')
                else:
                    block_value = self.field_matrix[row - int(self.border_num / 2)][col - int(self.border_num / 2)]
                # Zero value means empty space, so we display nothing
                if block_value != -1:
                    if block_value == 0:
                        # print(str(block_value), end='')
                        print(' ', end=' ')
                    # Displaying the rest of the values
                    else:
                        # print(str(block_value), end='')
                        print(block_value, end=' ')
            print()

    # Display score bar
    def display_score_bar(self, next_piece):
        # Score: XXX
        # Next piece: X
        print(f'Score: {self.score}')
        print(f'Next piece: {next_piece}')

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
    def update_matrix(self, check_block):

        block_value = self.get_block_value(check_block)
        linked_blocks = self.connected_blocks(check_block, set())

        if len(linked_blocks) > 2:
            cols_to_update = set()

            for block in linked_blocks:
                cols_to_update.add(block[1])
                self.change_block_value(block, 0)

            for col in cols_to_update:
                self.update_column(col)

            self.add_to_score(len(linked_blocks) * block_value)

    # Adding gravity to column blocks
    # TODO : add gravity columns which can be triggered
    def update_column(self, col):
        pass

    # For changing values of blocks
    def change_block_value(self, pos, value):
        self.field_matrix[pos[0]][pos[1]] = value

    # Return block value based on position
    def get_block_value(self, block):
        return self.field_matrix[block[0]][block[1]]

    # Get connected set of blocks with same value as origin
    # TODO : remove return? there is issue with branching
    def connected_blocks(self, ori_block, seen):
        seen.add(ori_block)
        next_to = self.get_adjacent_same(ori_block, self.get_block_value(ori_block))

        for pos in next_to:
            if pos not in seen:
                ori_block = pos
                return self.connected_blocks(ori_block, seen)

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

game = NewGame(number_of_rows, number_of_columns, score_to_win)
game.game_loop()
