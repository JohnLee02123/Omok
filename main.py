import pygame
from omokFiles.constants import RESET_EVENT, SETTINGS_EVENT, WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLS, BOARD_SIDE_PADDING, BOARD_START, BOARD_LENGTH
from omokFiles.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Omok')
    
settings = False
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    settings = False
    num = 0
    num1 = 0

    while run:
        clock.tick(FPS)

        #if game.winner() != None:
        #    print(game.winner())
        
        for event in pygame.event.get():
            num1 = 1
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == RESET_EVENT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                num += 1
                pos = pygame.mouse.get_pos()
                if not settings:
                    game.select(pos)
                else:
                    game.selectSettings(pos)
            
            if event.type == SETTINGS_EVENT:
                settings = True if settings == False else False
                num += 1
                num1 += 2


        if not settings:
            game.update()
        else:
            game.updateSettings()

    main()

if __name__ == "__main__":
    main()