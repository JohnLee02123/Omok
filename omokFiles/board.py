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
                self.b_potential[row].append(['o1', 'o1', 'o1', 'o1'])
                self.w_potential[row].append(['o1', 'o1', 'o1', 'o1'])
                self.b_defensible[row].append(['o1', 'o1', 'o1', 'o1'])
                self.w_defensible[row].append(['o1', 'o1', 'o1', 'o1'])
        for row in range(ROWS):
            self.b_potential[row][0] = 'c1'
            self.b_potential[row][COLS - 1] = 'c1'
            self.w_potential[row][0] = 'c1'
            self.w_potential[row][COLS - 1] = 'c1'
        for col in range(COLS):
            self.b_potential[0][col] = 'c1'
            self.b_potential[ROWS - 1][col] = 'c1'
            self.w_potential[0][col] = 'c1'
            self.w_potential[ROWS - 1][col] = 'c1'
        middle = ROWS // 2
        self.board[middle][middle] = 1        