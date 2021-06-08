import pygame
from omokFiles.constants import RESET_EVENT, WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLS, BOARD_SIDE_PADDING, BOARD_START, BOARD_LENGTH
from omokFiles.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Omok')
    

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
                pygame.quit()
            
            if event.type == RESET_EVENT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.select(pos)
            
        game.update()

    main()

if __name__ == "__main__":
    main()