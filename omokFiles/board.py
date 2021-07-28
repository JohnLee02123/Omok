import pygame
import os, json
import copy
from .constants import BLACK, BLACK_POTENTIAL, B_POT_TO_COLOR, DELTA, DIRTOIND, ILLEGAL_SQUARE, POT_FONT_CORR, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY, LINE_THICKNESS, BOARD_START, STONE_PADDING, POTENTIAL_FONT, POT_FONT_SIZE, POT_FONT_DIS, WHITE_POTENTIAL, W_POT_TO_COLOR
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
        self.bookKeepStack = []
        # self.file1 = open("debug.txt", "w")
    
    def copy(self):
        new = Board()
        new.board = copy.deepcopy(self.board)
        new.b_potential = copy.deepcopy(self.b_potential)
        new.w_potential = copy.deepcopy(self.w_potential)
        new.illegal = copy.deepcopy(self.illegal)
        new.draw_potential = copy.deepcopy(self.draw_potential)
        new.turn = copy.deepcopy(self.turn)
        new.num_move = copy.deepcopy(self.num_move)
        new.history = copy.deepcopy(self.history)
        new.redoHistory = copy.deepcopy(self.redoHistory)
        new.pot_to_square_b = copy.deepcopy(self.pot_to_square_b)
        new.pot_to_square_w = copy.deepcopy(self.pot_to_square_w)
        new.bookKeepStack = copy.deepcopy(self.bookKeepStack)

    def draw(self, win):
        self.draw_lines(win)
        self.draw_stones(win)
        self.draw_illegal(win)
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

    def draw_illegal(self, win):
        x, y = BOARD_START
        x += SQUARE_SIZE // 2
        y += SQUARE_SIZE // 2
        for i in range(ROWS):
            for j in range(COLS):
                if self.illegal[i][j] != ['na', 'na', 'na']:
                    win.blit(ILLEGAL_SQUARE, (x + j * SQUARE_SIZE - ILLEGAL_SQUARE.get_width()//2, y + i * SQUARE_SIZE - ILLEGAL_SQUARE.get_height()//2))

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
        pots = ['na', '00', 'c1', 'o1', 'c2', 'o2', 'c3', 'o3', 'c4', 'o4', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', 'x4']
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
        self.illegal[x][y] = ['na' for elem in self.illegal[x][y]]
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
        self.bookKeepStack.append(pos)
        while self.bookKeepStack:
            current = self.bookKeepStack.pop()
            for lane in lanes:
                self.bookKeepLane(current, lane, 1)
                self.bookKeepLane(current, lane, -1)
                
        self.updateJSON()

    def bookKeepLane(self, pos, dir, stone):
        i, j = pos
        dv, dh = DELTA[dir]
        length, iR, iC = self.getLaneInfo(pos, dir)
        ind = DIRTOIND[dir]
        longestPotLink = []
        count = 0
        bookKeepLater = []
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
                current += 1
            # elif num < 5:
            #     self.delDirection((iR + current * dv, iC + current * dh), num, stone, dir)
            #     current += num
            else:
                subarray = []
                if num < 5:
                    potentials = ['na'] * num
                elif num >= 5:
                    for a in range(num):
                        currRow = iR + (current + a) * dv
                        currCol = iC + (current + a) * dh
                        if stone == 1:
                            if self.board[currRow][currCol] == 0:
                                status = self.whichIllegal(currRow, currCol, ind)
                                subarray.append(status)
                            else:
                                subarray.append(1)
                        else:
                            subarray.append(self.board[iR + (current + a) * dv][iC + (current + a) * dh])
                    potentials = self.updatePotential(subarray, stone)
                # use potentials to update b_potential
                for a in range(num):
                    currRow = iR + (current + a) * dv
                    currCol = iC + (current + a) * dh
                    if potentials[a] == None:
                        if stone == 1:
                            self.pot_to_square_b[self.b_potential[currRow][currCol][ind]].remove((currRow, currCol, ind))
                            self.b_potential[currRow][currCol][ind] = 'na'
                            self.pot_to_square_b['na'].add((currRow, currCol, ind))
                        else:
                            self.pot_to_square_w[self.w_potential[currRow][currCol][ind]].remove((currRow, currCol, ind))
                            self.w_potential[currRow][currCol][ind] = 'na'
                            self.pot_to_square_w['na'].add((currRow, currCol, ind))
                    else:
                        if stone == 1:
                            self.pot_to_square_b[self.b_potential[currRow][currCol][ind]].remove((currRow, currCol, ind))
                            prevPot = self.b_potential[currRow][currCol][ind]
                            self.b_potential[currRow][currCol][ind] = potentials[a]
                            self.pot_to_square_b[potentials[a]].add((currRow, currCol, ind))
                            if self.detBookKeep(prevPot, potentials[a]):
                                bookKeepLater.append((currRow, currCol))

                            if potentials[a][0] == '0' and int(potentials[a][1]) > 5:
                                self.illegal[currRow][currCol][2] = 'il'
                            elif self.illegal[currRow][currCol][2] != "na":
                                ill = False
                                for i in range(4):
                                    check = self.b_potential[currRow][currCol][i]
                                    if check[0] == '0' and int(check[1]) > 5:
                                        ill = True
                                if not ill: # not illegal
                                    self.illegal[currRow][currCol][2] = "na"

                            if self.illegal[currRow][currCol][1] == "na": # not illegal (44) to start with
                                if self.b_potential[currRow][currCol][ind][1] == '4':
                                    count4 = self.black44(currRow, currCol)
                                    if count4 > 0:
                                        self.illegal[currRow][currCol][1] = '0' + str(count4)
                            else: # illegal (44) to start with
                                count4 = self.black44(currRow, currCol)
                                if count4 > 0:
                                    self.illegal[currRow][currCol][1] = '0' + str(count4)
                                else:
                                    self.illegal[currRow][currCol][1] = 'na'
                            
                            if self.illegal[currRow][currCol][0] == "na":
                                if self.b_potential[currRow][currCol][ind] == 'o3':
                                    count3 = self.black33(currRow, currCol)
                                    if count3 > 0:
                                        self.illegal[currRow][currCol][0] = '0' + str(count3)
                            else:
                                count3 = self.black33(currRow, currCol)
                                if count3 > 0:
                                    self.illegal[currRow][currCol][0] = '0' + str(count3)
                                else:
                                    self.illegal[currRow][currCol][0] = 'na'
                            
                            if prevPot == '05' and potentials[a] != '05':
                                count3 = self.black33(currRow, currCol)
                                if count3 > 0:
                                    self.illegal[currRow][currCol][0] = '0' + str(count3)
                                else:
                                    self.illegal[currRow][currCol][0] = 'na'
                                count4 = self.black44(currRow, currCol)
                                if count4 > 0:
                                    self.illegal[currRow][currCol][1] = '0' + str(count4)
                                else:
                                    self.illegal[currRow][currCol][1] = 'na'
                            elif potentials[a] == '05':
                                self.illegal[currRow][currCol] = ['na', 'na', 'na']
                        else:
                            self.pot_to_square_w[self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind]].remove((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                            self.w_potential[iR + (current + a) * dv][iC + (current + a) * dh][ind] = potentials[a]
                            self.pot_to_square_w[potentials[a]].add((iR + (current + a) * dv, iC + (current + a) * dh, ind))
                current += num
        for elem in bookKeepLater:
            self.bookKeepStack.append(elem)

    def detBookKeep(self, prevPot, pot):
        if prevPot == pot:
            return False
        if (prevPot != 'na' and (int(prevPot[1]) >= 4 or prevPot == 'o3')) or pot != 'na' and int(pot[1]) >= 4 or pot == 'o3':
            return True

    def whichIllegal(self, i, j, dirInd):
        count3 = 0
        count4 = 0
        countLong = 0
        for k in range(4):
            curr = self.b_potential[i][j][k]
            if k == dirInd or curr == 'na':
                continue
            if curr == 'c4' or curr == 'o4':
                count4 += 1
            elif curr == 'o3':
                count3 += 1
            elif curr == 'x4':
                return 10
            elif int(curr[1]) > 5 or curr[0] == '1':
                countLong += 1
        if count3 > 1 or count4 > 1 or countLong > 0:
            return 10
        elif count3 == 1:
            if count4 == 1:
                return 34
            else:
                return 3
        elif count4 == 1:
            return 4
        else:
            return 0

    def black44(self, i, j):
        count = 0
        for x in range(4):
            if self.b_potential[i][j][x] == 'c4' or self.b_potential[i][j][x] == 'o4':
                count += 1
            elif self.b_potential[i][j][x] == 'x4':
                count += 2
        return count if count > 1 else 0

    def black33(self, i, j):
        count = 0
        for x in range(4):
            if self.b_potential[i][j][x] == 'o3':
                count += 1
        return count if count > 1 else 0

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
        # print('        from updatePotential:')
        for a in range(len(subarray)):
            if subarray[a] == stone:
                ret.append(None)
            else:
                ret.append(self.potRec([subarray[:a], subarray[a+1:]], stone, False, a))
            # if subarray[a] == 0:
            #     app = self.potRec([subarray[:a], subarray[a+1:]], stone, False, 0)
            #     ret.append(app)
            # elif subarray[a] == 10:
            #     app = self.potRec([subarray[:a], subarray[a+1:]], stone, False, 0)
            #     ret.append(app)
            # else:
            #     ret.append(None)
        return ret

    def potRec(self, fbarr, stone, ill, base):
        if not ill:
            if stone == 1:
                if str((tuple(fbarr[0]), tuple(fbarr[1]), base)) in BLACK_POTENTIAL:
                    # print('already done', fbarr, stone, BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1])))])
                    return BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1]), base))]
            elif stone == 0:
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
            if base >= front0 + 1 and base <= flen + back0:
                return '0' + str(consec)
            else:
                return None
        # print('summary:', consec, fbarr, stone, ill, blockdir)
        
        
        nextFrontPot = None
        illegal = True
        front0 += 1 # to do the -= 1 inside
        while illegal and front0 != 0:
            front0 -= 1
            backarr = fbarr[0][front0+1:]
            backarr.append(stone)
            backarr.extend(fbarr[1].copy())
            if fbarr[0][front0] == 0:
                illegal = False
                nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone, False, base)
            elif fbarr[0][front0] == 10:
                nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone, True, base)
                if nextFrontPot == None:
                    continue
                else:
                    illegal = False
            elif fbarr[0][front0] == stone:
                continue
            else:
                nextFrontPot = self.potRec([fbarr[0][:front0], backarr], stone, False, base)
                if fbarr[0][front0] == 3 or fbarr[0][front0] == 34:
                    if nextFrontPot == 'o3':
                        continue
                if fbarr[0][front0] == 4 or fbarr[0][front0] == 34:
                    if nextFrontPot == 'c4' or nextFrontPot == 'o4':
                        continue
                illegal = False
        
        nextBackPot = None
        illegal = True
        back0 -= 1
        while illegal and back0 != blen - 1:
            back0 += 1
            frontarr = fbarr[0].copy()
            frontarr.append(stone)
            frontarr.extend(fbarr[1][:back0])
            if fbarr[1][back0] == 0:
                illegal = False
                nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone, False, base)
            elif fbarr[1][back0] == 10:
                nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone, True, base)
                if nextBackPot == None:
                    continue
                else:
                    illegal = False
            elif fbarr[1][back0] == stone:
                continue
            else:
                nextBackPot = self.potRec([frontarr, fbarr[1][back0+1:]], stone, False, base)
                if fbarr[1][back0] == 3 or fbarr[1][back0] == 34:
                    if nextBackPot == 'o3':
                        continue
                if fbarr[1][back0] == 4 or fbarr[1][back0] == 34:
                    if nextBackPot == 'c4' or nextBackPot == 'o4':
                        continue
                illegal = False
        if stone == 1:
            calc = self.calcPotBlack(nextFrontPot, nextBackPot)
            if calc == 'o4' and abs(back0 + (flen - front0 - 1)) != 3:
                calc = 'x4'
            # print('result: ', nextFrontPot, nextBackPot, calc, fbarr, stone, ill, blockdir)
            if not ill:
                BLACK_POTENTIAL[str((tuple(fbarr[0]), tuple(fbarr[1]), base))] = calc
            return calc
        else:
            calc = self.calcPotWhite(nextFrontPot, nextBackPot)
            # print('result: ', nextFrontPot, nextBackPot, calc)
            if not ill:
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