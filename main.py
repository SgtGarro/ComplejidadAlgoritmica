import pygame
from checkers.constants import WIDTH, HEIGHT,SQUARE_SIZE, RED, WHITE
from checkers.game import Game

FPS=60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
game = Game() 

# def get_row_col_from_mouse(pos):
#   x,y = pos
#   row = y// SQUARE_SIZE
#   col = x//SQUARE_SIZE
#   return row,col

def main():
    run = True
    clock = pygame.time.Clock()
   

    

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        game.draw(WINDOW)
        pygame.display.update()
    
    pygame.quit()

main()
