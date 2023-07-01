import pygame as py
from sys import exit
from constants import *
from engine import *

py.init()  # initialize pygame module

screen = py.display.set_mode((WIDTH, HEIGHT))   # set game screen
clock = py.time.Clock()                         # method that responsible for frame rates per second

py.display.set_caption("Chess Game")            # set game name
icon = py.image.load("images/bN.png")           # set game icon
py.display.set_icon(icon)                       # display game icon


# dictionary of pieces names (keys) which their values will be piece's image path
pieces_dict = {"wR": "", "wN": "", "wB": "", "wQ": "",
               "wK": "", "wp": "", "bR": "", "bN": "",
               "bB": "", "bQ": "", "bK": "", "bp": ""
               }


def main():

    upload_pieces()         # upload pieces images to be ready to display
    first_click = True      # first click (by default True) which mean that the user click on the first square
    second_click = False    # second click (by default False) which mean that the user click on the second square
    piece = Engine()        # create an objet "piece" which represent the piece that user click on

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if first_click:
                    x, y = py.mouse.get_pos()       # get square position
                    col = int(x//SQUARE_DI)         # get square col
                    row = int(y//SQUARE_DI)         # get square row
                    piece = Engine()
                    piece.row = row
                    piece.col = col
                    if Engine.board[row][col] == "*":   # if square selected is empty don't do anything
                        continue
                    else:                         # if square selected contain a piece then be ready to the second click
                        first_click = False
                        second_click = True
                        print("click first time")
                        continue

                if second_click:
                    x, y = py.mouse.get_pos()          # get second square position
                    col = int(x//SQUARE_DI)            # get second square col
                    row = int(y//SQUARE_DI)            # get second square row

                    Engine.make_move(piece, row, col)  # give the second square position to make_move method
                    second_click = False               # second click are done
                    first_click = True                 # be ready to the other first clicks

                    print("click second time")
                    continue

        draw_board()            # draw the chess board with right colors
        draw_pieces()           # draw the pieces on the board
        py.display.update()     # update screen
        clock.tick(60)          # refresh Screen 60 frames per second


def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            rect = py.Rect(row * SQUARE_DI, col * SQUARE_DI, SQUARE_DI, SQUARE_DI)
            if (row + col) % 2 == 0:
                py.draw.rect(screen, "#dad9b5", rect)

            else:
                py.draw.rect(screen, "#80a352", rect)


def upload_pieces():
    for key, value in pieces_dict.items():
        pieces_dict[key] = py.image.load("images/"+key+".png").convert_alpha()
        pieces_dict[key] = py.transform.scale(pieces_dict[key], (65, 65))


def draw_pieces():

    for row in range(ROWS):
        for col in range(COLS):
            if Engine.board[row][col] != "*":
                screen.blit(pieces_dict[Engine.board[row][col]], (col*SQUARE_DI, row*SQUARE_DI))


if __name__ == '__main__':
    main()
