import pygame
import os, json
from .constants import BLACK, BLACK_POTENTIAL, B_POT_TO_COLOR, DELTA, DIRTOIND, POT_FONT_CORR, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY, LINE_THICKNESS, BOARD_START, STONE_PADDING, POTENTIAL_FONT, POT_FONT_SIZE, POT_FONT_DIS, WHITE_POTENTIAL, W_POT_TO_COLOR
from collections import deque

class Board:
    def __init__(self):
        self.board = []
        self.b_potential = []
        self.w_potential = []
        self.draw_potential = 'n'
        self.create_board()
        self.turn = BLACK
        self.num_move = 0
        self.history = deque()
        self.potential_init()
    
    def draw(self, win):
        self.draw_lines(win)
        self.draw_stones(win)
        if self.draw_potential == 'b':
            self.draw_b_potential(win)
        if self.draw_potential == 'w':
            self.draw_w_potential(win)
    
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
    
    def draw_b_potential(self, win):
        x, y = BOARD_START
        x += SQUARE_SIZE // 2
        y += SQUARE_SIZE // 2
        for i in range(ROWS):
            for j in range(COLS):
                self.draw_single_b_potential(win, i, j, x + j * SQUARE_SIZE - POT_FONT_SIZE//2, y + i * SQUARE_SIZE - POT_FONT_SIZE//2)
    
    def draw_w_potential(self, win):
        x, y = BOARD_START
        x += SQUARE_SIZE // 2
        y += SQUARE_SIZE // 2
        for i in range(ROWS):
            for j in range(COLS):
                self.draw_single_w_potential(win, i, j, x + j * SQUARE_SIZE - POT_FONT_SIZE//2, y + i * SQUARE_SIZE - POT_FONT_SIZE//2)
    
    def draw_single_b_potential(self, win, i, j, x, y):
        t0 = POTENTIAL_FONT.render(self.b_potential[i][j][0], 1, B_POT_TO_COLOR[self.b_potential[i][j][0]])
        t1 = POTENTIAL_FONT.render(self.b_potential[i][j][1], 1, B_POT_TO_COLOR[self.b_potential[i][j][1]])
        t2 = POTENTIAL_FONT.render(self.b_potential[i][j][2], 1, B_POT_TO_COLOR[self.b_potential[i][j][2]])
        t3 = POTENTIAL_FONT.render(self.b_potential[i][j][3], 1, B_POT_TO_COLOR[self.b_potential[i][j][3]])
        win.blit(t0, (x + POT_FONT_DIS + POT_FONT_CORR, y - POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t1, (x - POT_FONT_DIS + POT_FONT_CORR, y - POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t2, (x - POT_FONT_DIS + POT_FONT_CORR, y + POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t3, (x + POT_FONT_DIS + POT_FONT_CORR, y + POT_FONT_DIS + POT_FONT_CORR))

    def draw_single_w_potential(self, win, i, j, x, y):
        t0 = POTENTIAL_FONT.render(self.w_potential[i][j][0], 1, W_POT_TO_COLOR[self.w_potential[i][j][0]])
        t1 = POTENTIAL_FONT.render(self.w_potential[i][j][1], 1, W_POT_TO_COLOR[self.w_potential[i][j][1]])
        t2 = POTENTIAL_FONT.render(self.w_potential[i][j][2], 1, W_POT_TO_COLOR[self.w_potential[i][j][2]])
        t3 = POTENTIAL_FONT.render(self.w_potential[i][j][3], 1, W_POT_TO_COLOR[self.w_potential[i][j][3]])
        win.blit(t0, (x + POT_FONT_DIS + POT_FONT_CORR, y - POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t1, (x - POT_FONT_DIS + POT_FONT_CORR, y - POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t2, (x - POT_FONT_DIS + POT_FONT_CORR, y + POT_FONT_DIS + POT_FONT_CORR))
        win.blit(t3, (x + POT_FONT_DIS + POT_FONT_CORR, y + POT_FONT_DIS + POT_FONT_CORR))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            self.b_potential.append([])
            self.w_potential.append([])
            for col in range(COLS):
                self.board[row].append(0)
                self.b_potential[row].append(['o1', 'o1', 'o1', 'o1'])
                self.w_potential[row].append(['o1', 'o1', 'o1', 'o1'])
    
    def potential_init(self):
        lanes = ['v', 'h', 'VH', 'vh']
        for lane in lanes:
            for i in range(ROWS):
                for j in range(COLS):
                    self.bookKeepLane((i, j), lane, 1)
                    self.bookKeepLane((i, j), lane, -1)
        self.updateJSON()

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def make_move(self, pos):
        x, y = pos
        if self.board[x][y] != 0:
            return False
        if self.turn == BLACK:
            i = 1
            for a in range(4):
                if self.b_potential[x][y][a] == '05':
                    print('black won!')
        else:
            i = -1
            for a in range(4):
                try:
                    num = int(self.w_potential[x][y][a])
                    if num >= 5:
                        print('white won!')
                except:
                    pass
        self.board[x][y] = i
        self.history.append(pos)
        self.moveBookKeep(pos)
        for i in range(4):
            self.b_potential[pos[0]][pos[1]][i] = 'na'
            self.w_potential[pos[0]][pos[1]][i] = 'na'
        self.change_turn()
        self.num_move += 1
    
    def undo(self):
        if len(self.history) == 0:
            return
        i, j = self.history.pop()
        self.board[i][j] = 0
        self.moveBookKeep((i, j))
        self.change_turn()
        self.num_move -= 1

    def moveBookKeep(self, pos):
        lanes = ['v', 'h', 'VH', 'vh']
        for lane in lanes:
            self.bookKeepLane(pos, lane, 1)
            self.bookKeepLane(pos, lane, -1)
        self.updateJSON()

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
            if self.board[iR + a * dv][iC + a * dh] == stone * -1:
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
                self.b_potential[iR + current * dv][iC + current * dh][ind] = 'na'
                current += 1
            elif num < 5:
                self.delDirection((iR + current * dv, iC + current * dh), num, stone, dir)
                current += num
            elif num >= 5:
                subarray = []
                for a in range(num):
                    subarray.append(self.board[iR + (current + a) * dv][iC + (current + a) * dh])
                potentials = self.updatePotential(subarray, stone)
                # use potentials to update b_potential
                # print('frombookkeeplane: ', subarray, potentials)
                for a in range(num):
                    if potentials[a] == None:
                        if stone == 1:
                            self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                        else:
                            self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                    else:
                        if stone == 1:
                            self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                        else:
                            self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
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
            if self.board[i + dv * a][j + dh * a] == 0:
                if stone == 1:
                    self.b_potential[i + dv * a][j + dh * a][ind] = '00'
                else:
                    self.w_potential[i + dv * a][j + dh * a][ind] = '00'

    def updatePotential(self, subarray, stone):
        ret = []
        for a in range(len(subarray)):
            if subarray[a] == 0:
                app = self.potRec([subarray[:a], subarray[a+1:]], stone)
                ret.append(app)
            else:
                ret.append(None)
        return ret

    def potRec(self, fbarr, stone):
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

    def updateJSON(self):
        with open(os.path.join('omokFiles', 'black_potential.json'), 'w') as fp1:
            json.dump(BLACK_POTENTIAL, fp1, indent = 4)
        with open(os.path.join('omokFiles', 'white_potential.json'), 'w') as fp2:
            json.dump(WHITE_POTENTIAL, fp2, indent = 4)