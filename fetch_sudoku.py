import requests
import random
import json
from copy import deepcopy

from solver import solve

url = 'https://sugoku.herokuapp.com/board?difficulty='
difficulties = ['easy', 'medium', 'hard']


def fetch():
    difficulty = random.choice(difficulties)
    res = requests.get(url + difficulty)
    if res.ok:
        return res.json()['board']
    return []


def main():
    for _ in range(100):
        dct = {}
        sudoku = fetch()
        un_solved = deepcopy(sudoku)

        if sudoku:
            solve(sudoku)

            dct['sudoku'] = un_solved 
            dct['solved'] = sudoku

            with open('sudoku.txt', 'a') as f:
                f.write(json.dumps(dct))
                f.write('\n')

if __name__ == '__main__':
    main()
