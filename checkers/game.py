import pygame
from pygame import Surface
from .board import Board
from .piece import Piece
from .constants import RED, WHITE


class Game:
    def __init__(self, window: Surface, board: Board) -> None:
        self.window = window
        self.board = board

        self.selected: Piece = None
        self.valid_moves = {}
        self.turn = RED

    def update(self):
        self.board.draw(self.valid_moves, self.window)
        pygame.display.update()

    def reset(self):
        self.board = Board()
        self.selected: Piece = None
        self.turn = RED
        self.valid_moves = {}

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(self.selected)
            return True

        return False

    def _move(self, row, col):
        target = self.board.get_piece(row, col)

        if self.selected and target == None and (row, col) in self.valid_moves:
            self.board.move(row, col, self.selected)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()
