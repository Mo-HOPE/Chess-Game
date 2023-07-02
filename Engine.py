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

    def __int__(self, row, col, new_row, new_col):

        self.row = row
        self.col = col
        self.new_row = new_row
        self.new_col = new_col

    # method that make a move on the board and switch roles between white and black
    def make_move(self):
        if self.valid_moves():
            if Engine.board[self.row][self.col][0] == "w":
                if Engine.white_turn:
                    Engine.board[self.new_row][self.new_col] = Engine.board[self.row][self.col]
                    Engine.moves_log.append(Engine.board[self.row][self.col])
                    Engine.board[self.row][self.col] = "*"
                    Engine.white_turn = False
                    Engine.black_turn = True

            if Engine.board[self.row][self.col][0] == "b":
                if Engine.black_turn:
                    Engine.board[self.new_row][self.new_col] = Engine.board[self.row][self.col]
                    Engine.moves_log.append(Engine.board[self.row][self.col])
                    Engine.board[self.row][self.col] = "*"
                    Engine.black_turn = False
                    Engine.white_turn = True

    def valid_moves(self):

        if Engine.board[self.row][self.col][1] == "p":
            return self.pawn_move()

        else:
            return True

    def pawn_move(self):

        # white pawn valid move
        if Engine.board[self.row][self.col][0] == "w":
            if Engine.board[self.new_row][self.new_col] != "w":
                if self.new_col != self.col:
                    return False

                if self.new_row == self.row-1:
                    return True

