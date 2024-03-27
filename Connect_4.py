import numpy as np
import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Paramètres de la fenêtre
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

# Création de la fenêtre
screen = pygame.display.set_mode(size)

# Fonction pour dessiner la grille
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Fonction pour afficher le tableau dans la console
def print_board(board):
    print(np.flip(board, 0))

# Fonction pour vérifier si une colonne est valide
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Fonction pour obtenir la prochaine ligne ouverte dans une colonne
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Fonction pour placer un jeton dans une colonne
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Fonction pour vérifier s'il y a une victoire
def winning_move(board, piece):
    # TODO: Implémenter la vérification de la victoire
    return False

# Fonction principale du jeu
def main():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    print_board(board)
    draw_board(board)  # Afficher la grille dès le début du jeu
    turn = 0

    # Boucle principale du jeu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # Demander au joueur 1 de jouer
                if turn == 0:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            print("Player 1 wins!")
                            pygame.quit()
                            sys.exit()
                    else:
                        print("Colonne déjà remplie. Choisissez une autre colonne.")
                        continue

                # Demander au joueur 2 de jouer
                else:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        if winning_move(board, 2):
                            print("Player 2 wins!")
                            pygame.quit()
                            sys.exit()
                    else:
                        print("Colonne déjà remplie. Choisissez une autre colonne.")
                        continue

                turn += 1
                turn %= 2
                print_board(board)
                draw_board(board)

if __name__ == "__main__":
    main()
