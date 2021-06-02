import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, LINE_THICKNESS, BOARD_START, STONE_PADDING

class Board:
    def __init__(self):
        self.board = []
        self.b_potential = []
        self.w_potential = []
        self.b_defensible = []
        self.w_defensible = []
        self.blackAttack = [None] * 6
        self.whiteAttack = [None] * 6
        self.create_board()
    
    def draw(self, win):
        self.draw_lines(win)
        self.draw_stones(win)
    
    def draw_lines(self, win):
        x, y = BOARD_START
        x += SQUARE_SIZE // 2
        y += SQUARE_SIZE // 2
        hEnd = x + (COLS - 1) * SQUARE_SIZE
        vEnd = y + (ROWS - 1) * SQUARE_SIZE
        for i in range(ROWS):
            pygame.draw.line(win, BLACK, (x, y + i * SQUARE_SIZE), (hEnd, y + i * SQUARE_SIZE), LINE_THICKNESS)
        for j in range(COLS):
            pygame.draw.line(win, BLACK, (x + j * SQUARE_SIZE, y), (x + j * SQUARE_SIZE, vEnd), LINE_THICKNESS)

    def draw_stones(self, win):
        x, y = BOARD_START
        x += SQUARE_SIZE // 2
        y += SQUARE_SIZE // 2
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == 1:
                    pygame.draw.circle(win, BLACK, (x + j * SQUARE_SIZE, y + i * SQUARE_SIZE), SQUARE_SIZE // 2 - STONE_PADDING)
                elif self.board[i][j] == -1:
                    pygame.draw.circle(win, WHITE, (x + j * SQUARE_SIZE, y + i * SQUARE_SIZE), SQUARE_SIZE // 2 - STONE_PADDING)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            self.b_potential.append([])
            self.w_potential.append([])
            self.b_defensible.append([])
            self.w_defensible.append([])
            for col in range(COLS):
                self.board[row].append(0)
                self.b_potential[row].append(None)
                self.w_potential[row].append(None)
                self.b_defensible[row].append(None)
                self.w_defensible[row].append(None)
        middle = ROWS // 2
        self.board[middle][middle] = 1
        