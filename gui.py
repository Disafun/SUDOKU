import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox,
    QProgressBar
)
from PyQt5.QtGui import QIntValidator, QIcon
from sudoku_generator import SudokuGenerator
from solver import SudokuSolver

# Устанавливаем путь к платформенным плагинам (если требуется)
plugin_path = os.path.join(
    os.path.dirname(sys.executable),
    'Lib',
    'site-packages',
    'PyQt5',
    'Qt',
    'plugins',
    'platforms'
)
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class SudokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Судоку')
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('icon.png'))

        self.grid = QGridLayout()
        self.cells = {}

        for i in range(9):
            for j in range(9):
                cell = QLineEdit(self)
                cell.setAlignment(Qt.AlignCenter)
                cell.setMaxLength(1)
                cell.setValidator(QIntValidator(1, 9))

                # Стилизация ячеек
                if (i // 3 + j // 3) % 2 == 0:
                    cell.setStyleSheet(
                        "background-color: #f0f0f0; border: 1px solid #c0c0c0;"
                        "font-size: 18px; font-weight: bold;"
                    )
                else:
                    cell.setStyleSheet(
                        "background-color: #ffffff; border: 1px solid #c0c0c0;"
                        "font-size: 18px; font-weight: bold;"
                    )
                self.grid.addWidget(cell, i, j)
                self.cells[(i, j)] = cell

        self.difficulty_selector = QComboBox(self)
        self.difficulty_selector.addItems(["Легкий", "Средний", "Сложный"])
        self.difficulty_selector.setCurrentIndex(1)

        self.generate_button = QPushButton('Сгенерировать', self)
        self.generate_button.setStyleSheet("font-size: 16px; padding: 5px;")
        self.generate_button.clicked.connect(self.start_loading)

        self.solve_button = QPushButton('Решить', self)
        self.solve_button.setStyleSheet("font-size: 16px; padding: 5px;")
        self.solve_button.clicked.connect(self.solve_sudoku)

        self.check_button = QPushButton('Проверить решение', self)
        self.check_button.setStyleSheet("font-size: 16px; padding: 5px;")
        self.check_button.clicked.connect(self.check_solution)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addWidget(self.difficulty_selector)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.solve_button)
        self.layout.addWidget(self.check_button)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

    def start_loading(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        value = self.progress_bar.value() + 5
        if value > 100:
            self.timer.stop()
            self.progress_bar.setVisible(False)
            self.generate_sudoku()
        else:
            self.progress_bar.setValue(value)

    def generate_sudoku(self):
        difficulty_map = {"Легкий": "easy", "Средний": "medium", "Сложный": "hard"}
        selected_difficulty = self.difficulty_selector.currentText()
        generator = SudokuGenerator()
        board = generator.generate(difficulty=difficulty_map[selected_difficulty])
        self.display_generated_board(board)

    def solve_sudoku(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)].text()
                if value:
                    row.append(int(value))
                else:
                    row.append(0)
            board.append(row)

        solver = SudokuSolver(board)
        if solver.solve():
            self.display_solution(solver.get_board())
        else:
            self.display_message("Не удалось найти решение!")

    def check_solution(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[(i, j)].text()
                if value:
                    row.append(int(value))
                else:
                    row.append(0)
            board.append(row)

        if self.is_valid_sudoku(board):
            self.display_message("Решение верное!")
        else:
            self.display_message("Решение неверное!")

    def is_valid_sudoku(self, board):
        def is_unique(group):
            group = [num for num in group if num != 0]
            return len(group) == len(set(group))

        for row in board:
            if not is_unique(row):
                return False

        for col in range(9):
            if not is_unique([board[row][col] for row in range(9)]):
                return False

        for block_row in range(0, 9, 3):
            for block_col in range(0, 9, 3):
                block = [
                    board[row][col]
                    for row in range(block_row, block_row + 3)
                    for col in range(block_col, block_col + 3)
                ]
                if not is_unique(block):
                    return False

        return True

    def display_generated_board(self, board):
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                if value != 0:
                    self.cells[(i, j)].setText(str(value))
                    self.cells[(i, j)].setReadOnly(True)
                else:
                    self.cells[(i, j)].clear()
                    self.cells[(i, j)].setReadOnly(False)

    def display_solution(self, solution):
        for i in range(9):
            for j in range(9):
                self.cells[(i, j)].setText(str(solution[i][j]))

    def display_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.setWindowTitle("Результат проверки")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuGUI()
    window.show()
    sys.exit(app.exec_())
