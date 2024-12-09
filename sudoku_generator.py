import random

class SudokuGenerator:
    def __init__(self):
        self.size = 9  # Размер стандартной сетки Судоку (9x9)
        self.board = [[0] * self.size for _ in range(self.size)]
        self.solution = None

    def generate(self, difficulty="medium"):
        """Генерирует новую головоломку с заданным уровнем сложности."""
        self.board = [[0] * self.size for _ in range(self.size)]
        self._fill_grid()
        self.solution = [row[:] for row in self.board]  # Сохраняем полное решение
        self._remove_numbers(difficulty)
        return self.board

    def _fill_grid(self):
        """Рекурсивное заполнение сетки судоку (на основе бэктрекинга)."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    random_numbers = list(range(1, 10))
                    random.shuffle(random_numbers)
                    for number in random_numbers:
                        if self._is_safe_to_place(i, j, number):
                            self.board[i][j] = number
                            if self._fill_grid():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def _is_safe_to_place(self, row, col, num):
        """Проверяет, можно ли безопасно поставить число num в ячейку (row, col)."""
        # Проверка строки и столбца
        if num in self.board[row]:
            return False
        if num in (self.board[i][col] for i in range(self.size)):
            return False
        # Проверка подгруппы 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def _remove_numbers(self, difficulty):
        """Удаляет числа из заполненной сетки в соответствии с уровнем сложности."""
        levels = {"easy": 40, "medium": 50, "hard": 60}  # Количество удаляемых чисел
        cells_to_remove = levels.get(difficulty, 50)  # По умолчанию "средний"
        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    def get_solution(self):
        """Возвращает полное решение текущей головоломки."""
        return self.solution

# Пример тестирования
if __name__ == "__main__":
    generator = SudokuGenerator()
    board = generator.generate(difficulty="medium")
    for row in board:
        print(row)
    print("\nSolution:")
    for row in generator.get_solution():
        print(row)
