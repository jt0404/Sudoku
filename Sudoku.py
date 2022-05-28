import pygame as pg 
import time 

from constants import *


class Sudoku:
    def __init__(self, sudoku, solved):
        self.sudoku = sudoku
        self.solved_sudoku = solved
        self.filled_squares = self._init_filled()
        self.starter_filled = self.filled_squares.copy()
        self.suggestions = {}
        self.highlighted = (-1, -1)
        self.solving = False 
        self.mistakes = 0
        self.solving_cell = (-1, -1)

    def _init_filled(self):
        filled = set()
        for row in range(9):
            for col in range(9):
                digit = self.sudoku[row][col]
                if digit:
                    filled.add((row, col))

        return filled 

    def set_highlighted(self, row, col):
        self.highlighted = row, col

    def set_solving(self):
        self.solving = not self.is_solved() 

    def is_solved(self):
        return self.sudoku == self.solved_sudoku

    def is_square_highlighted(self):
        row, col = self.highlighted
        return row in range(9) and col in range(9)

    def highlight_square(self, screen):
        offset = WIDTH//2 - SUDOKU_WIDTH//2
        if self.is_square_highlighted():
            row, col = self.highlighted
            x = col*CELL_WIDTH + offset 
            y = row*CELL_WIDTH + offset
            pg.draw.rect(screen, LIGHT_BLUE, (x, y, CELL_WIDTH, CELL_WIDTH))

    def suggest_digit(self, digit):
        if self.is_square_highlighted():
            row, col = self.highlighted
            if (row, col) not in self.filled_squares and self.sudoku[row][col] == 0:
                self.suggestions[row, col] = digit

    def insert_digit(self):
        row, col = self.highlighted
        if (row, col) in self.suggestions: 
            digit = self.suggestions[row, col]

            # if properly inserted digit
            if self.solved_sudoku[row][col] == digit:
                self.sudoku[row][col] = digit
                self.filled_squares.add((row, col))
            else:
                self.mistakes += 1
                
            del self.suggestions[row, col]

    def draw_mistakes(self, font, screen):
        txt1 = font.render('X: ', False, RED)
        txt2 = font.render(str(self.mistakes), False, BLACK)
        x1 = WIDTH//2 - SUDOKU_WIDTH//2
        y1 = HEIGHT//2 - SUDOKU_HEIGHT//2 - 40
        
        screen.blit(txt1, (x1, y1))
        screen.blit(txt2, (x1 + 40, y1))

    def draw_suggestions(self, font, screen):
        offset = WIDTH//2 - SUDOKU_WIDTH//2
        for row, col in self.suggestions:
            digit = self.suggestions[row, col]
            if digit:
                txt = font.render(str(digit), False, BLACK)
                x = col*CELL_WIDTH + offset + 2
                y = row*CELL_WIDTH + offset + 2
                screen.blit(txt, (x, y))

    def draw_digits(self, font, screen):
        offset = WIDTH//2 - SUDOKU_WIDTH//2 + CELL_WIDTH//2
        copied = self.filled_squares.copy()

        for row, col in copied:
            digit = self.sudoku[row][col]
            if digit:
                txt = font.render(str(digit), False, BLACK)
                x = col*CELL_WIDTH + offset - txt.get_width()//2 
                y = row*CELL_WIDTH + offset - txt.get_height()//2
                screen.blit(txt, (x, y))         

    def draw_solving_status(self, screen):
        offset = WIDTH//2 - SUDOKU_WIDTH//2
        if self.solving:
            row, col = self.solving_cell
            x = col*CELL_WIDTH + offset + 1
            y = row*CELL_WIDTH + offset + 1
            
            if self.solved_sudoku[row][col] == self.sudoku[row][col]:
                color = GREEN
            else:
                color = RED

            pg.draw.rect(screen, color, (x, y, CELL_WIDTH - 1, CELL_WIDTH - 1), 3)

    def draw_grid(self, screen):
        for i in range(10):            
            if i % 3:
                thickness = 1
            else:
                thickness = 4

            # horizontal lines 
            h_x = WIDTH//2 - SUDOKU_WIDTH//2 
            h_y = HEIGHT//2 - SUDOKU_HEIGHT//2 + i*CELL_WIDTH 
            pg.draw.line(screen, BLACK, (h_x, h_y), (h_x + SUDOKU_WIDTH, h_y), thickness)
            # vertical lines
            v_x = h_x + i*CELL_WIDTH
            v_y = HEIGHT//2 - SUDOKU_HEIGHT//2
            pg.draw.line(screen, BLACK, (v_x, v_y), (v_x, v_y + SUDOKU_HEIGHT), thickness) 

    # solver part
    def solve(self):
        row, col = self._get_free_cell()

        if row is None:
            return True

        self.solving_cell = (row, col)

        for digit in range(1, 10):
            if self._is_valid(row, col, digit):
                self.sudoku[row][col] = digit
                self.filled_squares.add((row, col))
                time.sleep(.1)

                if self.solve():
                    return True 

            self.sudoku[row][col] = 0
            self.filled_squares.discard((row, col))

        return False

    def _is_valid(self, row, col, digit):
        # check row
        if digit in self.sudoku[row]:
            return False

        # check column
        for i in range(9):
            if digit == self.sudoku[i][col]:
                return False 

        # check square 
        start_row = row//3 * 3
        start_col = col//3 * 3  

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if digit == self.sudoku[i][j]:
                    return False 

        return True

    def _get_free_cell(self):
        for row in range(9):
            for col in range(9):
                if self.sudoku[row][col] == 0:
                    return row, col 
        
        return None, None




                