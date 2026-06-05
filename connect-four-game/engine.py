import numpy as np

class ConnectFour:
    def __init__(self):
        self.ROWS = 6
        self.COLS = 7
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = 1  # Player 1 or Player 2 (-1)

    def clone(self):
        new_game = ConnectFour()
        new_game.board = np.copy(self.board)
        new_game.current_player = self.current_player
        return new_game

    def get_valid_moves(self):
        return [col for col in range(self.COLS) if self.board[0][col] == 0]

    def make_move(self, col):
        if self.board[0][col] != 0:
            raise ValueError(f"Column {col} is full!")
        
        # Apply gravity: find the lowest empty row
        for row in reversed(range(self.ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                break
        
        self.current_player = -self.current_player

    def check_winner(self):
        # Check horizontal
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                win = self.board[r][c] + self.board[r][c+1] + self.board[r][c+2] + self.board[r][c+3]
                if abs(win) == 4:
                    return self.board[r][c]

        # Check vertical
        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                win = self.board[r][c] + self.board[r+1][c] + self.board[r+2][c] + self.board[r+3][c]
                if abs(win) == 4:
                    return self.board[r][c]

        # Check positively sloped diagonals
        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                win = self.board[r][c] + self.board[r+1][c+1] + self.board[r+2][c+2] + self.board[r+3][c+3]
                if abs(win) == 4:
                    return self.board[r][c]

        # Check negatively sloped diagonals
        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                win = self.board[r][c] + self.board[r-1][c+1] + self.board[r-2][c+2] + self.board[r-3][c+3]
                if abs(win) == 4:
                    return self.board[r][c]

        # Check for draw
        if len(self.get_valid_moves()) == 0:
            return 0

        return None

    def render(self):
        symbols = {0: " . ", 1: " X ", -1: " O "}
        print("\n" + " ".join([f"[{i}]" for i in range(self.COLS)]))
        print("-" * 27)
        for row in self.board:
            print("".join([symbols[cell] for cell in row]))
        print("-" * 27)