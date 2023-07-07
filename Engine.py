class Engine:

    board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
             ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
             ["*", "*", "*", "*", "*", "*", "*", "*"],
             ["*", "*", "*", "*", "*", "*", "*", "*"],
             ["*", "*", "*", "*", "*", "*", "*", "*"],
             ["*", "*", "*", "*", "*", "*", "*", "*"],
             ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
             ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
             ]

    white_turn = True
    black_turn = False
    moves_log = []         # store all moves so we can undo later
    white_king_checked = False
    black_king_checked = False

    def __init__(self, row=0, col=0, new_row=0, new_col=0):

        self.row = row
        self.col = col
        self.new_row = new_row
        self.new_col = new_col

    # method that make a move on the board and switch roles between white and black
    def make_move(self):

        if self.valid_moves():
            if Engine.board[self.row][self.col][0] == "w":
                if Engine.white_turn:
                    data = (self.row, self.col, self.new_row, self.new_col,
                            Engine.board[self.row][self.col], Engine.board[self.new_row][self.new_col])
                    Engine.moves_log.append(data)
                    Engine.board[self.new_row][self.new_col] = Engine.board[self.row][self.col]
                    Engine.board[self.row][self.col] = "*"
                    Engine.white_turn = False
                    Engine.black_turn = True

            if Engine.board[self.row][self.col][0] == "b":
                if Engine.black_turn:
                    data = (self.row, self.col, self.new_row, self.new_col,
                            Engine.board[self.row][self.col], Engine.board[self.new_row][self.new_col])
                    Engine.moves_log.append(data)
                    Engine.board[self.new_row][self.new_col] = Engine.board[self.row][self.col]
                    Engine.board[self.row][self.col] = "*"
                    Engine.black_turn = False
                    Engine.white_turn = True

    def valid_moves(self) -> bool:

        pieces_moves = {"p": self.pawn_move(), "R": self.rock_move(), "N": self.knight_move(),
                        "B": self.bishop_move(), "Q": self.queen_move(), "K": self.king_move()
                        }

        return pieces_moves[Engine.board[self.row][self.col][1]]

    def under_attack(self):

        if Engine.white_turn:
            temp1, temp2 = self.new_row, self.new_col
            temp3, temp4 = self.row, self.col
            self.new_row, self.new_col = self.king_position()  # black king position
            break_loop = False
            for i in range(0, 8):
                for j in range(0, 8):
                    if Engine.board[i][j][0] == "w":
                        self.row = i
                        self.col = j
                        Engine.black_king_checked = self.valid_moves()
                        if Engine.black_king_checked:
                            break_loop = True
                            break
                if break_loop:
                    self.new_row = temp1
                    self.new_col = temp2
                    self.row = temp3
                    self.col = temp4
                    Engine.undo_move()
                    break

        elif Engine.black_turn:
            temp1, temp2 = self.new_row, self.new_col
            temp3, temp4 = self.row, self.col
            self.new_row, self.new_col = self.king_position()  # white king position
            break_loop = False
            for i in range(8):
                for j in range(8):
                    if Engine.board[i][j][0] == "b":
                        self.row = i
                        self.col = j
                        Engine.white_king_checked = self.valid_moves()
                        if Engine.white_king_checked:
                            break_loop = True
                            break
                if break_loop:
                    self.new_row = temp1
                    self.new_col = temp2
                    self.row = temp3
                    self.col = temp4
                    Engine.undo_move()
                    break

    def pawn_move(self) -> bool:

        can_move = False            # flag variable that will allow the pawn to move if all squares are empty
        # white pawn valid move

        if Engine.board[self.row][self.col][0] == "w":           # check if the piece is a white pawn
            if (Engine.board[self.new_row][self.new_col] == "*") and (self.col == self.new_col):  # empty square

                if self.row == 6:                                # if it's the first move, pawn can move twice or once
                    if (self.new_row == self.row-1) or (self.new_row == self.row-2):
                        can_move = True
                else:                                            # if it's not the first move, pawn can move just one
                    if self.new_row == self.row-1:
                        can_move = True

            if Engine.board[self.new_row][self.new_col][0] == "b":                   # attacking case
                if (self.new_row == self.row-1) and (self.new_col == self.col+1):    # take piece on the right
                    can_move = True
                elif (self.new_row == self.row-1) and (self.new_col == self.col-1):  # take piece on the left
                    can_move = True

            # en passant attack

        # black pawn valid moves
        if Engine.board[self.row][self.col][0] == "b":           # check if the piece is a black pawn
            if (Engine.board[self.new_row][self.new_col] == "*") and (self.col == self.new_col):  # empty square

                if self.row == 1:                                # if it's the first move, pawn can move twice or once
                    if (self.new_row == self.row+1) or (self.new_row == self.row+2):
                        can_move = True

                else:                                            # if it's not the first move, pawn can move just one
                    if self.new_row == self.row+1:
                        can_move = True

            if Engine.board[self.new_row][self.new_col][0] == "w":                   # attacking case
                if (self.new_row == self.row+1) and (self.new_col == self.col+1):    # take piece on the right
                    can_move = True
                elif (self.new_row == self.row+1) and (self.new_col == self.col-1):  # take piece on the left
                    can_move = True

        if can_move and (Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]):
            return True
        else:
            return False

    def en_passant(self) -> bool:

        can_take = False
        if Engine.board[self.row][self.col][0] == "w":                      # check if the piece is a white pawn
            if (Engine.board[self.new_row][self.new_col] == "*") and (self.col == self.new_col):    # empty square

                if (self.row == 6) and (self.new_row == self.row - 2):      # check if the white pawn move twice
                    can_take = False                                        # black pawn can capture by en passant

        elif Engine.board[self.row][self.col][0] == "w":                    # check if the piece is a white pawn
            if (Engine.board[self.new_row][self.new_col] == "*") and (self.col == self.new_col):  # empty square

                if (self.row == 6) and (self.new_row == self.row - 2):      # check if the white pawn move twice
                    can_take = False                                        # black pawn can capture by en passant

        if can_take:
            return True
        else:
            return False

    def rock_move(self) -> bool:

        can_move = False     # flag variable that will allow the rock to move if all squares are empty

        # moving up or down
        if (self.new_row != self.row) and (self.new_col == self.col):
            if self.new_row < self.row:                                 # moving up case
                if self.new_row == self.row-1:
                    if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                        can_move = True                                 # move one square
                else:

                    for i in range(self.new_row+1, self.row):
                        if Engine.board[i][self.col] == "*":            # check if all squares are empty
                            can_move = True
                        else:
                            can_move = False
                            break

            if self.new_row > self.row:                                 # moving down case
                if self.new_row == self.row + 1:
                    if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                        can_move = True                                 # move one square
                else:

                    for i in range(self.row+1, self.new_row):
                        if Engine.board[i][self.col] == "*":            # check if all squares are empty
                            can_move = True
                        else:
                            can_move = False
                            break

        # moving right or left
        if (self.new_row == self.row) and (self.new_col != self.col):
            if self.new_col < self.col:                                 # moving left case
                if self.new_col == self.col - 1:
                    if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                        can_move = True                                 # move one square
                else:

                    for i in range(self.new_col+1, self.col):
                        if Engine.board[self.row][i] == "*":            # check if all squares are empty
                            can_move = True
                        else:
                            can_move = False
                            break

            if self.new_col > self.col:                                 # moving right case
                if self.new_col == self.col + 1:
                    if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                        can_move = True                                 # move one square
                else:

                    for i in range(self.col+1, self.new_col):
                        if Engine.board[self.row][i] == "*":            # check if all squares are empty
                            can_move = True
                        else:
                            can_move = False
                            break

        if can_move and (Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]):
            return True
        else:
            return False

    def bishop_move(self) -> bool:

        can_move = False        # flag variable that will allow the rock to move if all squares are empty
        checker = 1             # counter that add one to row and col and check if they are empty or not

        if (self.new_row+self.new_col) % 2 == (self.row+self.col) % 2:              # same square color
            if (self.new_row != self.row) and (self.new_col != self.col):           # not moving vertical or horizontal

                if (self.new_row > self.row) and (self.new_col > self.col):             # moving down-right case
                    if (self.new_row == self.row+1) and (self.new_col == self.col+1):
                        if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                            can_move = True                                             # move one square
                    else:
                        if self.new_row - self.row == self.new_col - self.col:
                            for i in range(self.row+1, self.new_row):
                                if Engine.board[self.row+checker][self.col+checker] == "*":
                                    can_move = True                                     # check if all squares are empty
                                    checker += 1
                                else:
                                    can_move = False
                                    break

                elif (self.new_row > self.row) and (self.new_col < self.col):           # moving down-left case
                    if (self.new_row == self.row + 1) and (self.new_col == self.col - 1):
                        if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                            can_move = True                                             # move one square
                    else:
                        if self.new_row - self.row == self.col - self.new_col:
                            for i in range(self.row+1, self.new_row):
                                if Engine.board[self.row+checker][self.col-checker] == "*":
                                    can_move = True                                     # check if all squares are empty
                                    checker += 1
                                else:
                                    can_move = False
                                    break

                elif (self.new_row < self.row) and (self.new_col > self.col):           # moving up-right case
                    if (self.new_row == self.row - 1) and (self.new_col == self.col + 1):
                        if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                            can_move = True                                             # move one square
                    else:
                        if self.row-self.new_row == self.new_col-self.col:
                            for i in range(self.new_row+1, self.row):
                                if Engine.board[self.row-checker][self.col+checker] == "*":
                                    can_move = True                                     # check if all squares are empty
                                    checker += 1
                                else:
                                    can_move = False
                                    break

                elif (self.new_row < self.row) and (self.new_col < self.col):           # moving up-left case
                    if (self.new_row == self.row - 1) and (self.new_col == self.col - 1):
                        if Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]:
                            can_move = True                                             # move one square
                    else:
                        if self.row - self.new_row == self.col - self.new_col:
                            for i in range(self.new_row+1, self.row):
                                if Engine.board[self.row-checker][self.col-checker] == "*":
                                    can_move = True                                     # check if all squares are empty
                                    checker += 1
                                else:
                                    can_move = False
                                    break

        if can_move and (Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]):
            return True
        else:
            return False

    def queen_move(self) -> bool:

        return self.rock_move() or self.bishop_move()

    def knight_move(self) -> bool:

        can_move = False  # flag variable that will allow the knight to move if all squares are empty

        if (self.new_row != self.row) and (self.new_col != self.col):               # not moving vertical or horizontal

            if (self.new_row == self.row+1) and (self.new_col == self.col+2):       # moving case 1
                can_move = True

            elif (self.new_row == self.row+1) and (self.new_col == self.col-2):     # moving case 2
                can_move = True

            elif (self.new_row == self.row+2) and (self.new_col == self.col+1):     # moving case 3
                can_move = True

            elif (self.new_row == self.row+2) and (self.new_col == self.col-1):     # moving case 4
                can_move = True

            elif (self.new_row == self.row-1) and (self.new_col == self.col+2):     # moving case 5
                can_move = True

            elif (self.new_row == self.row-1) and (self.new_col == self.col-2):     # moving case 6
                can_move = True

            elif (self.new_row == self.row-2) and (self.new_col == self.col+1):     # moving case 7
                can_move = True

            elif (self.new_row == self.row-2) and (self.new_col == self.col-1):     # moving case 8
                can_move = True

        if can_move and (Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]):
            return True
        else:
            return False

    def king_move(self) -> bool:

        can_move = False  # flag variable that will allow the knight to move if all squares are empty

        if (self.new_row == self.row) and (self.new_col == self.col+1):             # moving case 1
            can_move = True

        elif (self.new_row == self.row) and (self.new_col == self.col-1):           # moving case 2
            can_move = True

        elif (self.new_row == self.row+1) and (self.new_col == self.col):           # moving case 3
            can_move = True

        elif (self.new_row == self.row+1) and (self.new_col == self.col+1):         # moving case 4
            can_move = True

        elif (self.new_row == self.row+1) and (self.new_col == self.col-1):         # moving case 5
            can_move = True

        elif (self.new_row == self.row-1) and (self.new_col == self.col):           # moving case 6
            can_move = True

        elif (self.new_row == self.row-1) and (self.new_col == self.col+1):         # moving case 7
            can_move = True

        elif (self.new_row == self.row-1) and (self.new_col == self.col-1):         # moving case 8
            can_move = True

        if can_move and (Engine.board[self.new_row][self.new_col][0] != Engine.board[self.row][self.col][0]):
            return True
        else:
            return False

    @classmethod
    def undo_move(cls):

        if len(Engine.moves_log) == 1:
            old_row, old_col, new_row, new_col, piece_moved, piece_captured = Engine.moves_log[0]
            Engine.board[old_row][old_col] = piece_moved
            Engine.board[new_row][new_col] = piece_captured
            Engine.moves_log.pop(0)

        if Engine.moves_log:
            old_row, old_col, new_row, new_col, piece_moved, piece_captured = Engine.moves_log[-1]
            Engine.board[old_row][old_col] = piece_moved
            Engine.board[new_row][new_col] = piece_captured
            Engine.moves_log.pop(-1)

        if Engine.white_turn:
            Engine.white_turn = False
            Engine.black_turn = True

        elif Engine.black_turn:
            Engine.black_turn = False
            Engine.white_turn = True

    @staticmethod
    def king_position() -> (int, int):

        # get king position (row and col)
        if Engine.white_turn:
            for i, row_elements in enumerate(Engine.board):
                for j, col_elements in enumerate(row_elements):
                    if col_elements == "bK":
                        return i, j

        elif Engine.black_turn:
            for i, row_elements in enumerate(Engine.board):
                for j, col_elements in enumerate(row_elements):
                    if col_elements == "wK":
                        return i, j
