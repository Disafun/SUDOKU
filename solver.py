class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        """ Решает судоку с использованием алгоритма backtracking. """
        return self.solve_sudoku(self.board)

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty(self, board):
        """ Ищет пустую ячейку в доске. """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, board, row, col, num):
        """ Проверяет, является ли число валидным для данной ячейки. """
        if num in board[row]:
            return False
        if num in [board[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def get_board(self):
        """ Возвращает доску """
        return self.board
