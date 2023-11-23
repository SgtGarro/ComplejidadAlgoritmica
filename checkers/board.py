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


class Board:
    def __init__(self) -> None:
        self.board: list[list[Piece | None]] = []
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
                field = Rect(
                    row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                )
                pygame.draw.rect(window, CREMA, field)

    def draw_pieces(self, window: Surface):
        for row in range(ROWS):
            for col in range(COLS):
                piece: Piece | None = self.board[row][col]
                if piece != None:
                    piece.draw(window)

    def draw_valid_moves(self, moves, window: Surface):
        for move in moves:
            row, col = move
            circle_coords = (
                col * SQUARE_SIZE + SQUARE_SIZE // 2,
                row * SQUARE_SIZE + SQUARE_SIZE // 2,
            )
            radius = SQUARE_SIZE // 2 - 30
            pygame.draw.circle(window, BLUE, circle_coords, radius)

    def draw(self, moves, window: Surface):
        self.draw_board(window)
        self.draw_pieces(window)
        self.draw_valid_moves(moves, window)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece != 0:
                if piece.color == RED:
                    self.red_pieces -= 1
                else:
                    self.white_pieces -= 1

    def winner(self):
        if self.red_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return RED

        return None

    def evaluate(self):
        return (
            self.white_pieces
            - self.red_pieces
            + self.white_queens * 0.5
            - self.red_pieces * 0.5
        )

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, row: int, col: int, piece: Piece):
        if not piece:
            return

        self.board[piece.row][piece.col], self.board[row][col] = (
            self.board[row][col],
            self.board[piece.row][piece.col],
        )

        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == WHITE:
                self.white_queens += 1
            else:
                self.red_queens += 1

    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]

    def get_valid_moves(self, piece: Piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.is_queen:
            moves.update(
                self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left)
            )
            moves.update(
                self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right)
            )
        if piece.color == WHITE or piece.is_queen:
            moves.update(
                self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left)
            )
            moves.update(
                self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right)
            )

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves: dict = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(
                        self._traverse_left(
                            r + step, row, step, color, left - 1, skipped=last
                        )
                    )
                    moves.update(
                        self._traverse_right(
                            r + step, row, step, color, left + 1, skipped=last
                        )
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves: dict = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(
                        self._traverse_left(
                            r + step, row, step, color, right - 1, skipped=last
                        )
                    )
                    moves.update(
                        self._traverse_right(
                            r + step, row, step, color, right + 1, skipped=last
                        )
                    )
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
