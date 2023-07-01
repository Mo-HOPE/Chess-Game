import pygame as py
from sys import exit
from constants import *
from engine import *

py.init()

screen = py.display.set_mode((WIDTH, HEIGHT))
clock = py.time.Clock()

py.display.set_caption("Chess Game")
icon = py.image.load("images/bN.png")
py.display.set_icon(icon)

pieces_dict = {"wR": "", "wN": "", "wB": "", "wQ": "",
               "wK": "", "wp": "", "bR": "", "bN": "",
               "bB": "", "bQ": "", "bK": "", "bp": ""
               }


def main():
    upload_pieces()
    first_click = True
    second_click = False
    piece = Engine()
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if first_click:
                    x, y = py.mouse.get_pos()
                    col = x//SQUARE_DI
                    row = y//SQUARE_DI
                    piece = Engine()
                    piece.row = int(row)
                    piece.col = int(col)
                    first_click = False
                    second_click = True
                    print("click first time")
                    continue

                if second_click:
                    x, y = py.mouse.get_pos()
                    col = x // SQUARE_DI
                    row = y // SQUARE_DI
                    Engine.make_move(piece, int(row), int(col))
                    first_click = True
                    second_click = False
                    print("click second time")
                    continue

        draw_board()
        draw_pieces()
        py.display.update()
        clock.tick(60)


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
