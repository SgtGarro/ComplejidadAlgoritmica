import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // ROWS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


# Colores de los campos del tablero
CREMA = (206, 180, 147)
MARRON = (57, 48, 39)


CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 40))
