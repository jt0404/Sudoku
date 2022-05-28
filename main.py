import pygame as pg
import threading
import json
import random
import time

from Sudoku import Sudoku
from constants import *

# pygame stuff 
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
pg.display.set_caption('Sudoku')
digit_font = pg.font.SysFont(FONT, DIGIT_FS)
suggestions_font = pg.font.SysFont(FONT, SUGGESTIONS_FS)
timer_font = pg.font.SysFont(FONT, TIMER_FS)
mistakes_font = pg.font.SysFont(FONT, MISTAKES_FS)

# game 
with open('sudoku.txt') as f:
    line = random.choice(f.readlines())
    dct = json.loads(line)

sudoku = Sudoku(dct['sudoku'], dct['solved'])
start = time.time()


# functions
def format_time():
    seconds = round(time.time() - start)
    s = seconds % 60
    m = seconds//60
    h = m//60
    return f'{h:02d}:{m:02d}:{s:02d}'


def handle_mouse(mx, my):
    offset = WIDTH//2 - SUDOKU_WIDTH//2
    row = (my - offset) // CELL_WIDTH
    col = (mx - offset) // CELL_WIDTH
    sudoku.set_highlighted(row, col)


def draw_time():
    timer = format_time()
    x = WIDTH//2 - SUDOKU_WIDTH//2
    y = HEIGHT//2 + SUDOKU_HEIGHT//2 + 15
    txt = timer_font.render('Time: ' + timer, False, BLACK)
    screen.blit(txt, (x, y))


def draw():
    screen.fill(WHITE)
    sudoku.highlight_square(screen)
    sudoku.draw_suggestions(suggestions_font, screen)
    sudoku.draw_digits(digit_font, screen)
    sudoku.draw_grid(screen)
    sudoku.draw_mistakes(mistakes_font, screen)
    sudoku.draw_solving_status(screen)
    draw_time()
    pg.display.update()


def main():
    run = True 

    while run:
        draw()
        clock.tick(FPS)
        pg.time.delay(DELAY)

        if sudoku.solving:
            sudoku.set_solving()
            continue

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False 
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = pg.mouse.get_pos()
                handle_mouse(mx, my)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_0 and sudoku.is_square_highlighted() or\
                    event.key == pg.K_BACKSPACE and sudoku.is_square_highlighted():
                    sudoku.suggest_digit(0) 
                elif event.key == pg.K_1:
                    sudoku.suggest_digit(1) 
                elif event.key == pg.K_2:
                    sudoku.suggest_digit(2) 
                elif event.key == pg.K_3:
                    sudoku.suggest_digit(3) 
                elif event.key == pg.K_4:
                    sudoku.suggest_digit(4) 
                elif event.key == pg.K_5:
                    sudoku.suggest_digit(5) 
                elif event.key == pg.K_6:
                    sudoku.suggest_digit(6) 
                elif event.key == pg.K_7:
                    sudoku.suggest_digit(7) 
                elif event.key == pg.K_8:
                    sudoku.suggest_digit(8) 
                elif event.key == pg.K_9:
                    sudoku.suggest_digit(9) 
                elif event.key == pg.K_RETURN:
                    sudoku.insert_digit()
                elif event.key == pg.K_SPACE:
                    sudoku.solving = True 
                    sudoku.suggestions.clear()
                    sudoku.set_highlighted(-1, -1)
                    threading.Thread(target=sudoku.solve).start()


if __name__ == '__main__':
    main()
            