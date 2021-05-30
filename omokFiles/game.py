import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE, BLACK, WOOD_BACKGROUND
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE

    def reset(self):
        self._init()

    def update(self):
        self.win.blit(WOOD_BACKGROUND, (0, 0))
        self.board.draw(self.win)
        #self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def select(self, pos):
        x, y = pos
        if self.board.board[x][y] != 0:
            return False
        i = 1 if self.turn == BLACK else -1
        self.board.board[x][y] = i
        self.change_turn()
        return True