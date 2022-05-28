def solve(board):
    row, col = get_free_cell(board)

    if row is None:
        return True

    for digit in range(1, 10):
        if is_valid(board, row, col, digit):
            board[row][col] = digit

            if solve(board):
                return True 

        board[row][col] = 0

    return False

def is_valid(board, row, col, digit):
    # check row
    if digit in board[row]:
        return False

    # check column
    for i in range(9):
        if digit == board[i][col]:
            return False 

    # check square 
    start_row = row//3 * 3
    start_col = col//3 * 3  

    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if digit == board[i][j]:
                return False 

    return True

def get_free_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col 
    
    return None, None
