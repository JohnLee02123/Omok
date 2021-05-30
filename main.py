import pygame
from omokFiles.constants import WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLS, BOARD_SIDE_PADDING, BOARD_START, BOARD_LENGTH
from omokFiles.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Omok')

def get_row_col_from_mouse(pos):
    x, y = pos
    bx, by = BOARD_START
    if x > bx and x <= bx + BOARD_LENGTH and y > by and y <= by + BOARD_LENGTH:
        return ((y - by) // SQUARE_SIZE, (x - bx) // SQUARE_SIZE)
    return None
    

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(FPS)

        #if game.winner() != None:
        #    print(game.winner())
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                newPos = get_row_col_from_mouse(pos)
                if newPos is not None:
                    print(newPos)
                    game.select(newPos)
            
        game.update()

    pygame.quit()

main()