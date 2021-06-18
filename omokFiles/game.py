from omokFiles.timer import Timer
import pygame
import os
import json
from .constants import CONSOLE_HEIGHT, CONSOLE_LENGTH, DEFAULT_FONT, DRAW_B_POT, DRAW_N_POT, DRAW_W_POT, GREEN_1, GREEN_2, RED, SETTINGS_BUTTON_HEIGHT, SETTINGS_BUTTON_PADDING, SETTINGS_BUTTON_WIDTH, SQUARE_SIZE, WHITE, BLUE, BLACK, WIDTH, WOOD_BACKGROUND, ROWS, COLS, DELTA, BLACK_POTENTIAL, DIRTOIND, WHITE_POTENTIAL, BOARD_START, BOARD_LENGTH
from .board import Board
from .utilities import Console, Panel, Settings_Button
from .settings import Settings

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.panel = Panel()
        self.console = Console()
        self.settingsButton = Settings_Button(WIDTH - SETTINGS_BUTTON_WIDTH - SETTINGS_BUTTON_PADDING, SETTINGS_BUTTON_PADDING, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT, GREEN_1, GREEN_2, "Settings", DEFAULT_FONT, BLACK)
        self.settings = Settings()
        self.timer = Timer()
        self.first = 0
        self.printlocal = True

    def reset(self):
        self._init()

    def update(self):
        self.win.blit(WOOD_BACKGROUND, (0, 0))
        self.board.draw(self.win)
        self.panel.draw(self.win, self.board.turn, self.board.num_move)
        self.console.draw(self.win)
        self.settingsButton.draw(self.win)
        self.timer.draw(self.win)
        pygame.display.update()
    
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
    
    def clicked_settings(self, pos):
        x, y = pos
        X, Y = self.settingsButton.x, self.settingsButton.y
        if x > X and x <= X + self.settingsButton.width and y > Y and y <= Y + self.settingsButton.height:
            return True
        return False

    def select(self, pos):
        newPos = self.get_row_col_from_mouse(pos)
        if newPos is not None:
            print(newPos)
            result = self.board.make_move(newPos)
            if result == "successful":
                self.timer.change_turn()
            return
        if self.clicked_console(pos):
            console_ret = self.console.click(pos)
            if console_ret == DRAW_B_POT:
                self.board.draw_potential = 'b'
            elif console_ret == DRAW_W_POT:
                self.board.draw_potential = 'w'
            elif console_ret == DRAW_N_POT:
                self.board.draw_potential = 'n'
            elif console_ret == "undo":
                self.board.undo()
                self.timer.change_turn()
            elif console_ret == "redo":
                self.board.redo()
                self.timer.change_turn()
        if self.clicked_settings(pos):
            self.settings.reset_parameters()
            self.settingsButton.press()


    def selectSettings(self, pos):
        x, y = pos
        X, Y = self.settings.x, self.settings.y
        if x > X and x <= X + self.settings.width and y > Y and y <= Y + self.settings.height:
            order = self.settings.click(pos)

    def updateSettings(self):
        self.settings.draw(self.win)
        pygame.display.update()