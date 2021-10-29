import copy


class Grid:

    start_pieces = {'O': [[[0, 4], [1, 4], [1, 5], [0, 5]]],
                    'I': [[[0, 4], [1, 4], [2, 4], [3, 4]], [[0, 3], [0, 4], [0, 5], [0, 6]]],
                    'S': [[[0, 5], [0, 4], [1, 4], [1, 3]], [[0, 4], [1, 4], [1, 5], [2, 5]]],
                    'Z': [[[0, 4], [0, 5], [1, 5], [1, 6]], [[0, 5], [1, 5], [1, 4], [2, 4]]],
                    'L': [[[0, 4], [1, 4], [2, 4], [2, 5]], [[0, 5], [1, 5], [1, 4], [1, 3]],
                          [[0, 4], [0, 5], [1, 5], [2, 5]], [[0, 6], [0, 5], [0, 4], [1, 4]]],
                    'J': [[[0, 5], [1, 5], [2, 5], [2, 4]], [[1, 5], [0, 5], [0, 4], [0, 3]],
                          [[0, 5], [0, 4], [1, 4], [2, 4]], [[0, 4], [1, 4], [1, 5], [1, 6]]],
                    'T': [[[0, 4], [1, 4], [2, 4], [1, 5]], [[0, 4], [1, 3], [1, 4], [1, 5]],
                          [[0, 5], [1, 5], [2, 5], [1, 4]], [[0, 4], [0, 5], [0, 6], [1, 5]]]}

    def __init__(self, cols, rows):
        self.can_move = False
        self.piece = None
        self.current_piece = []
        self.horizontal_move = 0
        self.vertical_move = 0
        self.rotation = 0
        self.rows = rows
        self.cols = cols
        self.current_max_rotation = None
        self.matrix = []
        for i in range(rows):
            self.matrix.append([])
            for j in range(cols):
                self.matrix[i].append('-')

    def print_matrix(self):
        print()
        for i in range(self.rows):
            print(*self.matrix[i])

    def rotate_piece(self):
        self.rotation += 1
        self.rotation %= self.current_max_rotation
        self.vertical_move += 1
        for j in range(4):
            self.current_piece[self.rotation][j][0] += self.vertical_move
            self.current_piece[self.rotation][j][1] += self.horizontal_move

    def move_down_piece(self):
        try:
            check_obstacle = [self.matrix[self.get_row_index(j) + 1][self.get_column_index(j)] == '0' for j in range(4)]
            if any(check_obstacle):
                self.can_move = False
            else:
                self.vertical_move += 1
                for j in range(4):
                    self.current_piece[self.rotation][j][0] += 1
        except IndexError:
            pass

    def move_left_piece(self):
        try:
            check_obstacle = [self.matrix[self.get_row_index(j)][self.get_column_index(j) - 1] == '0' for j in range(4)]
            if any(check_obstacle):
                self.can_move = False
            else:
                self.horizontal_move -= 1
                self.vertical_move += 1
                for j in range(4):
                    self.current_piece[self.rotation][j][0] += 1
                    self.current_piece[self.rotation][j][1] -= 1
        except IndexError:
            pass

    def right_move_piece(self):
        try:
            check_obstacle = [self.matrix[self.get_row_index(j)][self.get_column_index(j) + 1] == '0' for j in range(4)]
            if any(check_obstacle):
                self.can_move = False
            else:
                self.horizontal_move += 1
                self.vertical_move += 1
                for j in range(4):
                    self.current_piece[self.rotation][j][0] += 1
                    self.current_piece[self.rotation][j][1] += 1
        except IndexError:
            pass

    def create_new_piece(self):
        self.piece = str(input())
        self.current_piece = []
        self.current_piece = copy.deepcopy(Grid.start_pieces[self.piece])
        self.current_max_rotation = len(Grid.start_pieces[self.piece])
        self.can_move = True
        self.vertical_move = 0
        self.horizontal_move = 0
        self.rotation = 0

    def break_filled_rows(self):
        while self.matrix[self.rows - 1] == ['0' for _ in range(self.cols)]:
            for j in range(4):
                self.current_piece[self.rotation][j][0] += 1
            for j in reversed(range(1, self.rows)):
                self.matrix[j] = list(self.matrix[j - 1])

    def command_processing(self, command):
        if self.can_move:
            match command:
                case 'rotate':
                    self.rotate_piece()
                case 'down':
                    self.move_down_piece()
                case 'left':
                    self.move_left_piece()
                case 'right':
                    self.right_move_piece()
                case 'exit':
                    exit()
        else:
            match command:
                case 'piece':
                    self.create_new_piece()
                case 'break':
                    self.break_filled_rows()
                case 'exit':
                    exit()

    def check_left_border(self):
        check_left = [self.current_piece[self.rotation][j][1] >= 0 for j in range(4)]
        while not all(check_left):
            self.horizontal_move += 1
            for j in range(4):
                self.current_piece[self.rotation][j][1] += 1
            check_left = [self.current_piece[self.rotation][j][1] >= 0 for j in range(4)]

        check_left = [self.current_piece[self.rotation][j][0] !=
                      self.current_piece[self.rotation][j + 1][0] or
                      self.current_piece[self.rotation][j][1] !=
                      self.current_piece[self.rotation][j + 1][1] for j in range(3)]
        if not all(check_left):
            self.horizontal_move += 1
            for j in range(4):
                self.current_piece[self.rotation][j][1] += 1

    def check_right_border(self):
        check_right = [self.current_piece[self.rotation][j][1] < self.cols for j in range(4)]
        while not all(check_right):
            self.horizontal_move -= 1
            for j in range(4):
                self.current_piece[self.rotation][j][1] -= 1
            check_right = [self.current_piece[self.rotation][j][1] < self.cols for j in range(4)]

        check_right = [self.current_piece[self.rotation][j][0] !=
                       self.current_piece[self.rotation][j + 1][0] or
                       self.current_piece[self.rotation][j][1] !=
                       self.current_piece[self.rotation][j + 1][1] for j in range(3)]
        if not all(check_right):
            self.horizontal_move -= 1
            for j in range(4):
                self.current_piece[self.rotation][j][1] -= 1

    def check_down_border(self):
        check_down = [self.current_piece[self.rotation][j][0] < self.rows for j in range(4)]
        while not all(check_down):
            self.vertical_move -= 1
            for j in range(4):
                self.current_piece[self.rotation][j][0] -= 1
            check_down = [self.current_piece[self.rotation][j][0] < self.rows for j in range(4)]

        check_down = [self.current_piece[self.rotation][j][0] !=
                      self.current_piece[self.rotation][j + 1][0] or
                      self.current_piece[self.rotation][j][1] !=
                      self.current_piece[self.rotation][j + 1][1] for j in range(3)]
        if not all(check_down):
            self.vertical_move -= 1
            for j in range(4):
                self.current_piece[self.rotation][j][0] -= 1

        check_down = [self.current_piece[self.rotation][j][0] == self.rows - 1 for j in range(4)]
        if any(check_down):
            self.can_move = False

    def check_borders(self):
        self.check_left_border()
        self.check_right_border()
        self.check_down_border()

    def get_row_index(self, j):
        return self.current_piece[self.rotation][j][0]

    def get_column_index(self, j):
        return self.current_piece[self.rotation][j][1]

    def check_game_over(self):
        if not self.can_move:
            check_column = [self.matrix[0][i] == '0' for i in range(self.cols)]
            if any(check_column):
                print('\nGame Over!')
                exit()

    def logic(self):
        self.print_matrix()
        self.command_processing(str(input()))
        while True:

            for j in range(4):
                try:
                    self.matrix[self.get_row_index(j)][self.get_column_index(j)] = '0'

                except IndexError:
                    pass
            self.print_matrix()
            self.check_game_over()
            if self.can_move:
                for j in range(4):
                    self.matrix[self.get_row_index(j)][self.get_column_index(j)] = '-'

            self.command_processing(str(input()))
            if self.can_move:
                self.check_borders()


first_command = input().split()
grid = Grid(int(first_command[0]), int(first_command[1]))
grid.logic()
