import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE, BLACK, WOOD_BACKGROUND, ROWS, COLS
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
    
    def moveBookKeeping(self, pos):
        x, y = pos
    
    def bookKeepingInitBlack(self, pos):
        i, j = pos
        self.board.board.b_potential[i][j] = 0
        longestPotLink = []
        count = 0
        for a in range(0, ROWS):
            if self.board.board[a][j] == -1:
                longestPotLink.append(count)
                longestPotLink.append(-1)
                count = 0
            else:
                count += 1
        longestPotLink.append(count)
        current = 0
        for num in longestPotLink:
            if num == 0:
                continue
            elif num == -1:
                current += 1
            elif num < 5:
                
                current += num
            elif num == 5:
                countRock = 0
                emptyPos = []
                for a in range(5):
                    if self.board.board[current + a][j] == 1:
                        countRock += 1
                    else:
                        emptyPos.append((current + a, j))
                if countRock == 3:
                    if self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]] is not None:
                        self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]]['v'] = 'c4'
                    else:
                        self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]] = {'v':'c4'}
                    if self.board.b_potential[emptyPos[1][0]][emptyPos[1][1]] is not None:
                        self.board.b_potential[emptyPos[1][0]][emptyPos[1][1]]['v'] = 'c4'
                    else:
                        self.board.b_potential[emptyPos[1][0]][emptyPos[1][1]] = {'v':'c4'}
                elif countRock == 4:
                    if self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]] is not None:
                        self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]]['v'] = '5'
                    else:
                        self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]] = {'v': '5'}
                current += 5
            elif num > 5:
                

        # if num < 5, don't do anything
        # if num == 5, if there are 3 inside, the rest are closed 4s. If there are 4 inside, the leftover is a 5
        # if num < 6:
        #    

        if self.board.b_potential[i][j]['v'] is not None:
    def 