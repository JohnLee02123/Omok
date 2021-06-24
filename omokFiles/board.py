import pygame
import os, json
from .constants import BLACK, BLACK_POTENTIAL, B_POT_TO_COLOR, DELTA, DIRTOIND, POT_FONT_CORR, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY, LINE_THICKNESS, BOARD_START, STONE_PADDING, POTENTIAL_FONT, POT_FONT_SIZE, POT_FONT_DIS, WHITE_POTENTIAL, W_POT_TO_COLOR
from collections import deque

class Board:
    def __init__(self):
        self.board = []
        self.b_potential = []
        self.w_potential = []
        self.illegal = []
        self.draw_potential = 'n'
        self.create_board()
        self.turn = BLACK
        self.num_move = 0
        self.history = deque()
        self.redoHistory = deque()
        self.pot_to_square_b = {}
        self.pot_to_square_w = {}
        self.pot_to_square_init()
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
            self.illegal.append([])
            for col in range(COLS):
                self.board[row].append(0)
                self.b_potential[row].append(['na', 'na', 'na', 'na'])
                self.w_potential[row].append(['na', 'na', 'na', 'na'])
                self.illegal[row].append(['na', 'na', 'na']) # 0 is 33, 1 is 44, 2 is 6+
    
    def pot_to_square_init(self):
        lanes = [0, 1, 2, 3]
        pots = ['na', '00', 'c1', 'o1', 'c2', 'o2', 'c3', 'o3', 'c4', 'o4', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
        for pot in pots:
            self.pot_to_square_b[pot] = set()
            self.pot_to_square_w[pot] = set()
        for lane in lanes:
            for i in range(ROWS):
                for j in range(COLS):
                    self.pot_to_square_b['na'].add((i, j, lane))
                    self.pot_to_square_w['na'].add((i, j, lane))

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
            return "slot not empty"
        if self.turn == BLACK:
            i = 1
            if self.illegal[x][y] != ['na', 'na', 'na']:
                return "illegal"
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
        if len(self.redoHistory) > 0:
            self.redoHistory.clear()
        self.moveBookKeep(pos)
        for i in range(4):
            self.pot_to_square_b[self.b_potential[pos[0]][pos[1]][i]].remove((pos[0], pos[1], i))
            self.b_potential[pos[0]][pos[1]][i] = 'na'
            self.pot_to_square_b['na'].add((pos[0], pos[1], i))
            self.pot_to_square_w[self.w_potential[pos[0]][pos[1]][i]].remove((pos[0], pos[1], i))
            self.w_potential[pos[0]][pos[1]][i] = 'na'
            self.pot_to_square_w['na'].add((pos[0], pos[1], i))
        self.change_turn()
        self.num_move += 1
        return "successful"
        # for key in self.pot_to_square_b.keys():
        #     print(key, len(self.pot_to_square_b[key]), len(self.pot_to_square_w[key]), self.pot_to_square_b[key], self.pot_to_square_w[key])
    
    def undo(self):
        if len(self.history) == 0:
            return
        pos = self.history.pop()
        self.redoHistory.append(pos)
        self.board[pos[0]][pos[1]] = 0
        self.moveBookKeep(pos)
        self.change_turn()
        self.num_move -= 1
    
    def redo(self):
        if len(self.redoHistory) == 0:
            return
        pos = self.redoHistory.pop()
        self.history.append(pos)
        if self.turn == BLACK:
            self.board[pos[0]][pos[1]] = 1
        else:
            self.board[pos[0]][pos[1]] = -1
        self.moveBookKeep(pos)
        for i in range(4):
            self.pot_to_square_b[self.b_potential[pos[0]][pos[1]][i]].remove((pos[0], pos[1], i))
            self.b_potential[pos[0]][pos[1]][i] = 'na'
            self.pot_to_square_b['na'].add((pos[0], pos[1], i))
            self.pot_to_square_w[self.w_potential[pos[0]][pos[1]][i]].remove((pos[0], pos[1], i))
            self.w_potential[pos[0]][pos[1]][i] = 'na'
            self.pot_to_square_w['na'].add((pos[0], pos[1], i))
        self.change_turn()
        self.num_move += 1

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
        # print('bookKeepLane:', pos, dir, length, iR, iC)
        longestPotLink = []
        count = 0
        bookKeepLater = []
        for a in range(0, length):
            if self.board[iR + a * dv][iC + a * dh] == stone * -1: # or (stone == 1 and self.illegal[iR + a * dv][iC + a * dh] != ['na', 'na', 'na'])
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
                #self.pot_to_square[self.b_potential[iR + current * dv][iC + current * dh][ind]].remove((iR + current * dv, iC + current * dh, ind))
                #self.b_potential[iR + current * dv][iC + current * dh][ind] = 'na'
                #self.pot_to_square['na'].add((iR + current * dv, iC + current * dh, ind))
                current += 1
            elif num < 5:
                self.delDirection((iR + current * dv, iC + current * dh), num, stone, dir)
                current += num
            elif num >= 5:
                subarray = []
                for a in range(num):
                    if stone == 1 and self.illegal[iR + (current + a) * dv][iC + (current + a) * dh] != ['na', 'na', 'na']:
                        subarray.append(10) # added to deal with illegal cases
                    else:
                        subarray.append(self.board[iR + (current + a) * dv][iC + (current + a) * dh])
                potentials = self.updatePotential(subarray, stone)
                # use potentials to update b_potential
                # print('frombookkeeplane: ', subarray, potentials)
                for a in range(num):
                    if potentials[a] == None:
                        if stone == 1:
                            self.pot_to_square_b[self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind]].remove((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                            self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                            self.pot_to_square_b['na'].add((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                        else:
                            self.pot_to_square_w[self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind]].remove((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                            self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = 'na'
                            self.pot_to_square_w['na'].add((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                    else:
                        if stone == 1:
                            self.pot_to_square_b[self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind]].remove((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                            self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                            if self.illegal[iR + (current + a) * dv][iC + (current + a) * dh][2] == "na": # not illegal (>5) to start with
                                if potentials[a][0] == '0' and int(potentials[a][1]) > 5:
                                    self.illegal[iR + (current + a) * dv][iC + (current + a) * dh][2] = "il"
                                    bookKeepLater.append((iR + (current + a) * dv, iC + (current + a) * dh))
                            else: # illegal (>5) to start with
                                ill = False
                                for i in range(4):
                                    check = self.b_potential[iR + (current + a) * dv][iC + (current + a) * dh][i]
                                    if check[0] == '0' and int(check[1]) > 5:
                                        ill = True
                                if not ill: # not illegal anymore
                                    self.illegal[iR + (current + a) * dv][iC + (current + a) * dh][2] = "na"
                                    bookKeepLater.append((iR + (current + a) * dv, iC + (current + a) * dh))
                            self.pot_to_square_b[potentials[a]].add((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                        else:
                            self.pot_to_square_w[self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind]].remove((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                            self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                            self.pot_to_square_w[potentials[a]].add((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                current += num
        # for elem in bookKeepLater:
        #     self.moveBookKeep(elem)

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
                    self.pot_to_square_b[self.b_potential[i + dv * a][j + dh * a][ind]].remove((i + dv * a, j + dh * a, ind))
                    self.b_potential[i + dv * a][j + dh * a][ind] = '00'
                    self.pot_to_square_b['00'].add((i + dv * a, j + dh * a, ind))
                else:
                    self.pot_to_square_w[self.w_potential[i + dv * a][j + dh * a][ind]].remove((i + dv * a, j + dh * a, ind))
                    self.w_potential[i + dv * a][j + dh * a][ind] = '00'
                    self.pot_to_square_w['00'].add((i + dv * a, j + dh * a, ind))

    def updatePotential(self, subarray, stone):
        ret = []
        print('        from updatePotential:')
        for a in range(len(subarray)):
            if subarray[a] == 0:
                print('   calling potrec from updatepotential', [subarray[:a], subarray[a+1:]], False)
                app = self.potRec([subarray[:a], subarray[a+1:]], stone, False, 0)
                ret.append(app)
            elif subarray[a] == 10:
                print('   calling potrec from updatepotential', [subarray[:a], subarray[a+1:]], True)
                app = self.potRec([subarray[:a], subarray[a+1:]], stone, True, 0)
                ret.append(app)
            else:
                ret.append(None)
        return ret

    def potRec(self, fbarr, stone, ill, blockdir):
        if blockdir == 0 and not ill:
            if stone == 1:
                if str((tuple(fbarr[0]), tuple(fbarr[1]))) in BLACK_POTENTIAL:
                    print('already done', fbarr, stone, BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))])
                    return BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
            else:
                if str((tuple(fbarr[0]), tuple(fbarr[1]))) in WHITE_POTENTIAL:
                    return WHITE_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))]
        flen = len(fbarr[0])
        blen = len(fbarr[1])
        front0 = -1 # includes illegal and zero
        back0 = blen
        for a in range(flen):
            if fbarr[0][flen - 1 - a] != stone:
                front0 = flen - 1 - a
                break
        for a in range(blen):
            if fbarr[1][a] != stone:
                back0 = a
                break
        consec = back0 + (flen - front0 - 1) + 1
        if ill:
            if consec == 5:
                return '05'
            else:
                return None
        if consec >= 5:
            return '0' + str(consec)
        print('summary:', consec, fbarr, stone, ill, blockdir)
        if front0 != -1: # if there's anything left in the front
            backarr = fbarr[0][front0+1:]
            backarr.append(stone)
            backarr.extend(fbarr[1].copy())
            print('in front')
            if fbarr[0][front0] == 10:
                print('front0 is illegal')
                if blockdir != -1:
                    print('   not blockdir, call potRec for illegal: ')
                    nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone, True, 0)
                    print('   returned from potrec for illegal')
                    if nextFrontPot == None:
                        print('illegal checked, 5 not possible')
                        frontZero = -1
                        for a in range(flen):
                            if fbarr[0][flen - 1 - a] == 0:
                                frontZero = flen - 1 - a
                                break
                        if frontZero != -1:
                            backarr = fbarr[0][frontZero+1:]
                            backarr.append(1)
                            backarr.extend(fbarr[1].copy())
                            print('   frontZero exists, call potRec on the zero')
                            nextFrontPot = self.potRec([fbarr[0][:frontZero], backarr], stone, False, -1)
                            print('   returned from potrec')
                        else:
                            print('frontZero is -1, nextFrontPot = None')
                            nextFrontPot = None
                else:
                    print('blockdir == -1')
                    nextFrontPot = None
            else:
                print('   front0 is not illegal, call potRec on the zero')
                nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone, False, 0)
                print('return from potRec')
        else:
            print('nothing in front')
            nextFrontPot = None
        if back0 != blen: # if there's anything left in the back
            frontarr = fbarr[0].copy()
            frontarr.append(stone)
            frontarr.extend(fbarr[1][:back0])
            print('in back')
            if fbarr[1][back0] == 10:
                print('back0 is illegal')
                if blockdir != 1:
                    print('   not blockdir, call potRec for illegal: ')
                    nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone, True, 0)
                    print('   returned from potrec for illegal')
                    if nextBackPot == None:
                        backZero = blen
                        print('illegal checked, 5 not possible')
                        for a in range(blen):
                            if fbarr[1][a] == 0:
                                backZero = a
                                break
                        if backZero != blen:
                            frontarr = fbarr[0].copy()
                            frontarr.append(1)
                            frontarr.extend(fbarr[1][:backZero])
                            print('   backZero exists, call potRec on the zero')
                            nextBackPot = self.potRec([frontarr, fbarr[1][backZero+1:]], stone, False, 1)
                            print('   returned from potrec')
                        else:
                            print('backZero is -1, nextFrontPot = None')
                            nextBackPot = None
                else:
                    print('blockdir == -1')
                    nextBackPot = None
            else:
                print('   back0 is not illegal, call potRec on the zero')
                nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone, False, 0)
                print('   returned from potRec')
        else:
            print('nothing in back')
            nextBackPot = None
        # if self.printlocal:
        #     print(nextFrontPot, nextBackPot, fbarr)
        if stone == 1:
            calc = self.calcPotBlack(nextFrontPot, nextBackPot)
            print('result: ', nextFrontPot, nextBackPot, calc, fbarr, stone, ill, blockdir)
            if blockdir == 0 and not ill:
                BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))] = calc
            return calc
        else:
            calc = self.calcPotWhite(nextFrontPot, nextBackPot)
            print('result: ', nextFrontPot, nextBackPot, calc)
            if blockdir == 0 and not ill:
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