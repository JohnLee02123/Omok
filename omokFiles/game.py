import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE, BLACK, WOOD_BACKGROUND, ROWS, COLS, DELTA, POTENTIAL
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
        #self.board.b_potential[i][j] = 0
            # calculate slots in which combos can be formed (vertical)
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

            # calculate possible combos (vertical)
        current = 0
        for num in longestPotLink:
            if num == 0:
                continue
            elif num == -1:
                current += 1
            elif num < 5:
                self.delDirection((current, j), num, BLACK, 'v')
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
                    self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]][0] = 'c4'
                    self.board.b_potential[emptyPos[1][0]][emptyPos[1][1]][0] = 'c4'
                elif countRock == 4:
                    self.board.b_potential[emptyPos[0][0]][emptyPos[0][1]][0] = '05'
                current += 5
            elif num > 5:
                subarray = []
                for a in range(num):
                    subarray.append(self.board.board[current + a][j])
                potentials = self.updateBlackPotential(subarray)
                # use potentials to update b_potential
                current += num


        # if num < 5, don't do anything
        # if num == 5, if there are 3 inside, the rest are closed 4s. If there are 4 inside, the leftover is a 5
        # if num < 6:
        #    

    def delDirection(self, pos, num, color, dir):
        i, j = pos
        dv, dh = DELTA[dir]
        for a in range(num):
            if self.board.board[i + dv * a][j + dh * a] == 0:
                if color == BLACK:
                    self.board.b_potential[i + dv * a][j + dh * a][0] = '00'
                else:
                    self.board.w_potential[i + dv * a][j + dh * a][0] = '00'
    
    def updateBlackPotential(self, subarray):
        ret = []
        for a in range(len(subarray)):
            if subarray[a] == 0:
                ret.append(self.blackPotRec([subarray[:a], subarray[a+1:]]))
            else:
                ret.append(0)

    def blackPotRec(self, fbarr):
        if str((tuple(fbarr[0]), tuple(fbarr[1]))) in POTENTIAL:
            return POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
        flen = len(fbarr[0])
        blen = len(fbarr[1])
        front0 = 0
        back0 = blen
        for a in range(flen):
            if fbarr[0][flen - 1 - a] == 0:
                front0 = flen - 1 - a
                break
        for a in range(blen):
            if fbarr[1][a] == 0:
                back0 = a
                break
        consec = back0 + (flen - front0 - 1) + 1
        if consec >= 5:
            return '0' + str(consec)
        if front0 != 0:
            backarr = fbarr[0][front0+1:]
            backarr.append(1)
            backarr.extend(fbarr[1])
            nextFrontPot = self.blackPotRec(self, [fbarr[0][:front0], backarr])
        else:
            nextFrontPot = None
        if back0 != blen:
            frontarr = fbarr[0]
            frontarr.append(1)
            frontarr.extend(fbarr[1][:back0])
            nextBackPot = self.blackPotRec(self, [frontarr, fbarr[1][back0+1:]])
        else:
            nextBackPot = None
        if nextFrontPot is None:
            if nextBackPot == '05':
                return 'c4'
            elif nextBackPot == 'c4':
                return 'c3'
            elif nextBackPot == 'c3':
                return 'c2'
            elif nextBackPot == 'c2':
                return 'c1'
        elif nextBackPot is None:
            if nextFrontPot == '05':
                return 'c4'
            elif nextFrontPot == 'c4':
                return 'c3'
            elif nextFrontPot == 'c3':
                return 'c2'
            elif nextFrontPot == 'c2':
                return 'c1'
        else:
            if nextBackPot == '05' and nextFrontPot == '05':
                return 'o4'
            elif nextBackPot == '05' or nextFrontPot == '05':
                return 'c4'
            elif nextBackPot == 'o4' or nextFrontPot == 'o4':
                return 'o3'
            elif nextBackPot == 'c4' or nextFrontPot == 'c4':
                return 'c3'
            elif nextBackPot == 'o3' or nextBackPot == 'o3':
                return 'o2'
            elif nextBackPot == 'c3' or nextBackPot == 'c3':
                return 'c2'
            elif nextBackPot == 'o2' or nextBackPot == 'o2':
                return 'o1'
            elif nextBackPot == 'c2' or nextBackPot == 'c2':
                return 'c1'