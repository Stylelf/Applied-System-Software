import numpy as np
import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Window parameters
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Player names
PLAYER_NAMES = ["Player 1", "Player 2"]

class GameWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

    def draw_board(self, board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(self.screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()

class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = np.zeros((rows, columns))

    def print_board(self):
        print(np.flip(self.grid, 0))

    def is_valid_location(self, col):
        return self.grid[self.rows - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.grid[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def check_winner(self, piece):
        # Check horizontal locations for win
        for c in range(self.columns - 3):
            for r in range(self.rows):
                if self.grid[r][c] == piece and self.grid[r][c + 1] == piece and self.grid[r][c + 2] == piece and self.grid[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if self.grid[r][c] == piece and self.grid[r + 1][c] == piece and self.grid[r + 2][c] == piece and self.grid[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.columns - 3):
            for r in range(self.rows - 3):
                if self.grid[r][c] == piece and self.grid[r + 1][c + 1] == piece and self.grid[r + 2][c + 2] == piece and self.grid[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.columns - 3):
            for r in range(3, self.rows):
                if self.grid[r][c] == piece and self.grid[r - 1][c + 1] == piece and self.grid[r - 2][c + 2] == piece and self.grid[r - 3][c + 3] == piece:
                    return True

        return False

class Player:
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

    def make_move(self, board, col):
        if board.is_valid_location(col):
            row = board.get_next_open_row(col)
            board.drop_piece(row, col, self.marker)
            return True
        return False

def main():
    board = Board(ROW_COUNT, COLUMN_COUNT)
    window = GameWindow(width, height)
    board.print_board()
    window.draw_board(board.grid)
    turn = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.quit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(window.screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(window.screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(window.screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if board.is_valid_location(col):
                    row = board.get_next_open_row(col)
                    board.drop_piece(row, col, 1 if turn == 0 else 2)

                    if board.check_winner(1 if turn == 0 else 2):
                        window.draw_board(board.grid)
                        font = pygame.font.SysFont("monospace", 75)
                        label = font.render(f"{PLAYER_NAMES[turn]} wins!", 1, RED if turn == 0 else YELLOW)
                        window.screen.blit(label, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        window.quit()

                    turn += 1
                    turn %= 2
                    board.print_board()
                    window.draw_board(board.grid)
                else:
                    print("Column already full. Please choose another column.")

if __name__ == "__main__":
    main()
