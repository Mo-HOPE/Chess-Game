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

    def __int__(self, row, col):

        self.row = row
        self.col = col

    def make_move(self, new_row, new_col):
        Engine.board[new_row][new_col] = Engine.board[self.row][self.col]
        Engine.board[self.row][self.col] = "*"
