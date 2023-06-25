import pygame as py
from sys import exit
from constants import *

py.init()

screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Chess Game")

clock = py.time.Clock()

icon = py.image.load("images/bN.png")
py.display.set_icon(icon)


def main():

    while True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                exit()
        for row in range(ROWS):
            for col in range(COLS):
                rect = py.Rect(row*SQUARE_DI,col*SQUARE_DI,SQUARE_DI,SQUARE_DI)
                if (row+col)%2 == 0:
                    py.draw.rect(screen,'white',rect)

                else:
                    py.draw.rect(screen, 'black', rect)
        py.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
