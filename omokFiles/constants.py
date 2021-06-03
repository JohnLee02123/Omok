import pygame
import os
import json

WIDTH, HEIGHT = 600, 780
ROWS = 15
COLS = ROWS
BOARD_SIDE_PADDING = 20
SQUARE_SIZE = (WIDTH - BOARD_SIDE_PADDING * 2) // ROWS
BOARD_BOTTOM_PADDING = 40
BOARD_LENGTH = WIDTH - BOARD_SIDE_PADDING * 2
BOARD_START = (BOARD_SIDE_PADDING, HEIGHT - (BOARD_LENGTH + BOARD_BOTTOM_PADDING))

LINE_THICKNESS = 2
STONE_PADDING = 2
DELTA = {'v': (1,0), 'VH': (1,1), 'h': (0,1), 'vh': (-1, 1)}

WOOD_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'wood_background.jpg')), (WIDTH, HEIGHT))

with open(os.path.join('omokFiles', 'potential.json')) as json_file:
    POTENTIAL = json.load(json_file)

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)