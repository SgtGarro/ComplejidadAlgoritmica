from .constants import SQUARE_SIZE, CROWN
from pygame import Surface
import pygame

class Piece:
    def __init__(self, row, col, color) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.is_queen = False
    
    def make_queen(self):
        self.is_queen = True
    
    def draw(self, window: Surface):
        radius = SQUARE_SIZE // 2 - 20
        coord_x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        coord_y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(window, self.color, (coord_x, coord_y), radius)

        if self.is_queen:
            window.blit(CROWN, (coord_x - CROWN.get_width() // 2, coord_y - CROWN.get_height() // 2))
