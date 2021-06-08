import pygame
import os
import json
from .constants import CONSOLE_HEIGHT, CONSOLE_LENGTH, DRAW_B_POT, DRAW_N_POT, DRAW_W_POT, RED, SQUARE_SIZE, WHITE, BLUE, BLACK, WOOD_BACKGROUND, ROWS, COLS, DELTA, BLACK_POTENTIAL, DIRTOIND, WHITE_POTENTIAL, BOARD_START, BOARD_LENGTH
from .board import Board
from .utilities import Console, Panel

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.panel = Panel()
        self.console = Console()
        self.turn = BLACK
        self.first = 0
        self.printlocal = True
        self.num_move = 0
        self.potential_init()

    def reset(self):
        self._init()

    def update(self):
        self.win.blit(WOOD_BACKGROUND, (0, 0))
        self.board.draw(self.win)
        self.panel.draw(self.win, self.turn, self.num_move)
        self.console.draw(self.win)
        #self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
    
    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def get_row_col_from_mouse(self, pos):
        x, y = pos
        bx, by = BOARD_START
        if x > bx and x <= bx + BOARD_LENGTH and y > by and y <= by + BOARD_LENGTH:
            return ((y - by) // SQUARE_SIZE, (x - bx) // SQUARE_SIZE)
        return None

    def clicked_console(self, pos):
        x, y = pos
        cx, cy = self.console.x, self.console.y
        if x > cx and x <= cx + CONSOLE_LENGTH and y > cy and y <= cy + CONSOLE_HEIGHT:
            return True
        return False

    def select(self, pos):
        newPos = self.get_row_col_from_mouse(pos)
        if newPos is not None:
            print(newPos)
            self.make_move(newPos)
            return
        if self.clicked_console(pos):
            console_ret = self.console.click(pos)
            if console_ret == DRAW_B_POT:
                self.board.draw_potential = 'b'
            elif console_ret == DRAW_W_POT:
                self.board.draw_potential = 'w'
            elif console_ret == DRAW_N_POT:
                self.board.draw_potential = 'n'

    def make_move(self, pos):
        x, y = pos
        if self.board.board[x][y] != 0:
            return False
        if self.turn == BLACK:
            i = 1
            for a in range(4):
                if self.board.b_potential[x][y][a] == '05':
                    print('black won!')
        else:
            i = -1
            for a in range(4):
                try:
                    num = int(self.board.w_potential[x][y][a])
                    if num >= 5:
                        print('white won!')
                except:
                    pass
        self.board.board[x][y] = i
        self.moveBookKeep(pos)
        self.change_turn()
        self.num_move += 1
        return True
    
    def potential_init(self):
        lanes = ['v', 'h', 'VH', 'vh']
        for lane in lanes:
            for i in range(ROWS):
                for j in range(COLS):
                    self.bookKeepLane((i, j), lane, 1)
                    self.bookKeepLane((i, j), lane, -1)
        self.updateJSON()

    def moveBookKeep(self, pos):
        lanes = ['v', 'h', 'VH', 'vh']
        for lane in lanes:
            self.bookKeepLane(pos, lane, 1)
            self.bookKeepLane(pos, lane, -1)
        for i in range(4):
            self.board.b_potential[pos[0]][pos[1]][i] = 'na'
            self.board.w_potential[pos[0]][pos[1]][i] = 'na'
        self.updateJSON()
        
    def updateJSON(self):
        with open(os.path.join('omokFiles', 'black_potential.json'), 'w') as fp1:
            json.dump(BLACK_POTENTIAL, fp1, indent = 4)
        with open(os.path.join('omokFiles', 'white_potential.json'), 'w') as fp2:
            json.dump(WHITE_POTENTIAL, fp2, indent = 4)


    def bookKeepLane(self, pos, dir, stone):
        i, j = pos
        dv, dh = DELTA[dir]
        length, iR, iC = self.getLaneInfo(pos, dir)
        ind = DIRTOIND[dir]
            # calculate slots in which combos can be formed (vertical)
        # print('bookKeepLane:', pos, dir, length, iR, iC)
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
                potentials = self.updatePotential(subarray, stone)
                # use potentials to update b_potential
                # print('frombookkeeplane: ', subarray, potentials)
                for a in range(num):
                    if potentials[a] == None:
                        if stone == 1:
                            self.board.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                        else:
                            self.board.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                    else:
                        if stone == 1:
                            self.board.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                        else:
                            self.board.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
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
    
    def updatePotential(self, subarray, stone):
        ret = []
        for a in range(len(subarray)):
            if subarray[a] == 0:
                app = self.potRec([subarray[:a], subarray[a+1:]], stone)
                if self.first == 10000:
                    self.printlocal = False
                # if self.printlocal:
                #     print(app)
                ret.append(app)
                self.first += 1
            else:
                ret.append(None)
        return ret

    def potRec(self, fbarr, stone):
        # if self.printlocal:
        #     print(fbarr)
        if stone == 1:
            if str((tuple(fbarr[0]), tuple(fbarr[1]))) in BLACK_POTENTIAL:
                return BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
        else:
            if str((tuple(fbarr[0]), tuple(fbarr[1]))) in WHITE_POTENTIAL:
                return WHITE_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
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
            nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone)
        else:
            nextFrontPot = None
        if back0 != blen:
            frontarr = fbarr[0].copy()
            frontarr.append(1)
            frontarr.extend(fbarr[1][:back0])
            nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone)
        else:
            nextBackPot = None
        # if self.printlocal:
        #     print(nextFrontPot, nextBackPot, fbarr)
        if stone == 1:
            calc = self.calcPotBlack(nextFrontPot, nextBackPot)
            BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))] = calc
            return calc
        else:
            calc = self.calcPotWhite(nextFrontPot, nextBackPot)
            WHITE_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))] = calc
            return calc


    def calcPotBlack(self, front, back):
        if front is None:
            if back == '05':
                return 'c4'
            elif back == 'c4':
                return 'c3'
            elif back == 'c3':
                return 'c2'
            elif back == 'c2':
                return 'c1'
        elif back is None:
            if front == '05':
                return 'c4'
            elif front == 'c4':
                return 'c3'
            elif front == 'c3':
                return 'c2'
            elif front == 'c2':
                return 'c1'
        else:
            if back == '05' and front == '05':
                return 'o4'
            elif back == '05' or front == '05':
                return 'c4'
            elif back == 'o4' or front == 'o4':
                return 'o3'
            elif back == 'c4' or front == 'c4':
                return 'c3'
            elif back == 'o3' or front == 'o3':
                return 'o2'
            elif back == 'c3' or front == 'c3':
                return 'c2'
            elif back == 'o2' or front == 'o2':
                return 'o1'
            elif back == 'c2' or front == 'c2':
                return 'c1'
        # if self.printlocal:
        #     print('wow got here', front, back)
        return '00'

    def calcPotWhite(self, front, back):
        iback, ifront = 0, 0
        try:
            iback = int(back)
        except:
            pass
        try:
            ifront = int(front)
        except:
            pass
        if front is None:
            if iback >= 5:
                return 'c4'
            elif back == 'c4':
                return 'c3'
            elif back == 'c3':
                return 'c2'
            elif back == 'c2':
                return 'c1'
        elif back is None:
            if ifront >= 5:
                return 'c4'
            elif front == 'c4':
                return 'c3'
            elif front == 'c3':
                return 'c2'
            elif front == 'c2':
                return 'c1'
        else:
            if iback >= 5 and ifront >= 5:
                return 'o4'
            elif iback >= 5 or ifront >= 5:
                return 'c4'
            elif back == 'o4' or front == 'o4':
                return 'o3'
            elif back == 'c4' or front == 'c4':
                return 'c3'
            elif back == 'o3' or front == 'o3':
                return 'o2'
            elif back == 'c3' or front == 'c3':
                return 'c2'
            elif back == 'o2' or front == 'o2':
                return 'o1'
            elif back == 'c2' or front == 'c2':
                return 'c1'
        # if self.printlocal:
        #     print('wow got here', front, back)
        return '00'