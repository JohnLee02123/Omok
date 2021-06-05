import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE, BLACK, WOOD_BACKGROUND, ROWS, COLS, DELTA, POTENTIAL, DIRTOIND
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.first = 0
        self.printlocal = True

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
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        self.moveBookKeep(pos)
        self.change_turn()
        return True
    
    def moveBookKeep(self, pos):
        stones = [1]
        lanes = ['v', 'h', 'VH', 'vh']
        for stone in stones:
            for lane in lanes:
                self.bookKeepLane(pos, lane, stone)

    def bookKeepLane(self, pos, dir, stone):
        i, j = pos
        dv, dh = DELTA[dir]
        length, iR, iC = self.getLaneInfo(pos, dir)
        ind = DIRTOIND[dir]
            # calculate slots in which combos can be formed (vertical)
        print('bookKeepLane:', pos, dir, stone, length, iR, iC)
        longestPotLink = []
        count = 0
        for a in range(0, length):
            if self.board.board[iR + a * dv][iC + a * dh] == stone * -1:
                longestPotLink.append(count)
                longestPotLink.append(-1)
                count = 0
            else:
                count += 1
        longestPotLink.append(count)
            # calculate possible combos
        current = 0
        for num in longestPotLink:
            if num == 0:
                continue
            elif num == -1:
                self.board.b_potential[iR + current * dv][iC + current * dh][ind] = 'na'
                current += 1
            elif num < 5:
                self.delDirection((iR + current * dv, iC + current * dh), num, stone, dir)
                current += num
            elif num >= 5:
                subarray = []
                for a in range(num):
                    subarray.append(self.board.board[iR + (current + a) * dv][iC + (current + a) * dh])
                potentials = self.updateBlackPotential(subarray)
                # use potentials to update b_potential
                print('frombookkeeplane: ', subarray, potentials)
                for a in range(num):
                    if potentials[a] == None:
                        self.board.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                    else:
                        self.board.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                current += num

    def getLaneInfo(self, pos, dir):
        i, j = pos
        if dir == 'v':
            length = ROWS
            iR, iC = 0, j
        elif dir == 'h':
            length = COLS
            iR, iC = i, 0
        elif dir == 'VH':
            if i - j >= 0:
                length = ROWS - (i - j)
                iR, iC = i - j, 0
            else:
                length = ROWS - (j - i)
                iR, iC = 0, j - i
        else:
            if i + j >= ROWS:
                length = 2 * ROWS - 1 - i - j
                iR, iC = ROWS - 1, j - (ROWS - 1 - i)
            else:
                length = i + j + 1
                iR, iC = i + j, 0
        return (length, iR, iC)

    def delDirection(self, pos, num, stone, dir):
        i, j = pos
        dv, dh = DELTA[dir]
        ind = DIRTOIND[dir]
        for a in range(num):
            if self.board.board[i + dv * a][j + dh * a] == 0:
                if stone == 1:
                    self.board.b_potential[i + dv * a][j + dh * a][ind] = '00'
                else:
                    self.board.w_potential[i + dv * a][j + dh * a][ind] = '00'
    
    def updateBlackPotential(self, subarray):
        ret = []
        for a in range(len(subarray)):
            if subarray[a] == 0:
                app = self.blackPotRec([subarray[:a], subarray[a+1:]])
                if self.first == 10000:
                    self.printlocal = False
                if self.printlocal:
                    print(app)
                ret.append(app)
                self.first += 1
            else:
                ret.append(None)
        return ret

    def blackPotRec(self, fbarr):
        if self.printlocal:
            print(fbarr)
        if str((tuple(fbarr[0]), tuple(fbarr[1]))) in POTENTIAL:
            return POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
        flen = len(fbarr[0])
        blen = len(fbarr[1])
        front0 = -1
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
        if front0 != -1:
            
            backarr = fbarr[0][front0+1:]
            backarr.append(1)
            backarr.extend(fbarr[1].copy())
            nextFrontPot = self.blackPotRec([fbarr[0][:front0], backarr])
        else:
            nextFrontPot = None
        if back0 != blen:
            frontarr = fbarr[0].copy()
            frontarr.append(1)
            frontarr.extend(fbarr[1][:back0])
            nextBackPot = self.blackPotRec([frontarr, fbarr[1][back0+1:]])
        else:
            nextBackPot = None
        if self.printlocal:
            print(nextFrontPot, nextBackPot, fbarr)
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
        return '00'
        if self.printlocal:
            print('wow got here', nextFrontPot, nextBackPot, fbarr)