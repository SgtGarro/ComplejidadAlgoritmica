import pygame
from pygame import Surface, Rect
from .piece import Piece
from .constants import *


# [0, 1, 0, 1, 0, 1, 0, 1],
# [1, 0, 1, 0, 1, 0, 1, 0],
# [0, 1, 0, 1, 0, 1, 0, 1],
# [0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0],
# [2, 0, 2, 0, 2, 0, 2, 0],
# [0, 2, 0, 2, 0, 2, 0, 2],
# [2, 0, 2, 0, 2, 0, 2, 0],

class Game:
    def __init__(self) -> None:
        self.board = []
        self.current_piece = None
        self.red_pieces = 12
        self.white_pieces = 12
        self.red_queens = 0
        self.white_queens = 0
        self.init_board()

    def init_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def draw_board(self, window: Surface):
        window.fill(MARRON)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                field = Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(window, CREMA, field)
    def draw_pieces(self, window: Surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece: Piece | None = self.board[row][col]
                if piece != None:
                    piece.draw(window)

    def draw(self, window: Surface):
        self.draw_board(window)
        self.draw_pieces(window)
