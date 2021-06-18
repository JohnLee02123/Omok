import pygame
import os
import json
import copy
import omokFiles.constants as constants
from .utilities import Button, Display, Display_Only_Text, Settings_Button
from .constants import BLACK, BUTTON_INT_PADDING, BUTTON_PADDING, DEFAULT_FONT, GREEN_1, GREEN_2, GREY, GREY_1, GREY_2, GREY_3, RESET_EVENT, NEW_SETTINGS, SAVE_RESTART_BUTTON_HEIGHT, SAVE_RESTART_BUTTON_WIDTH, SETTINGS, SETTINGS_BUTTON_HEIGHT, SETTINGS_BUTTON_WIDTH, SETTINGS_EVENT, SETTINGS_HEIGHT, SETTINGS_INT_PADDING, SETTINGS_PADDING, SETTINGS_PADDING, SETTINGS_TITLE_FONT_SIZE, SETTINGS_WIDTH, SETT_TIME_DISP_HEIGHT, SETT_TIME_DISP_WIDTH

class Settings():
    def __init__(self):
        self.x, self.y = SETTINGS_PADDING, SETTINGS_PADDING
        self.width, self.height = SETTINGS_WIDTH, SETTINGS_HEIGHT
        self.changed = False
        self.all_Buttons = []
        self.etc_Buttons = []
        self.col1 = []
        self._initialize()
        self.set_all_col_positions()
    
    def _initialize(self):
        self.closeButton = Close_Settings_Button(self.x + self.width - BUTTON_PADDING - SETTINGS_BUTTON_WIDTH, self.y + BUTTON_PADDING, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT, GREEN_1, GREEN_1, "Close", DEFAULT_FONT, BLACK)
        self.save_restart_button = Save_Restart_Button(self.x + self.width - BUTTON_PADDING - SAVE_RESTART_BUTTON_WIDTH, self.y + self.height - BUTTON_PADDING - SAVE_RESTART_BUTTON_HEIGHT, SAVE_RESTART_BUTTON_WIDTH, SAVE_RESTART_BUTTON_HEIGHT, GREEN_2, GREEN_2, "Save and Restart", DEFAULT_FONT, BLACK)
        self.etc_Buttons.extend([self.closeButton, self.save_restart_button])
        self.all_Buttons.extend([self.closeButton, self.save_restart_button])

        self.title1 = Display_Only_Text(0, 0, SETTINGS_TITLE_FONT_SIZE, "Time per move", DEFAULT_FONT, BLACK)
        self.black_time_display = Display_Settings_Black_Time(0, 0, SETT_TIME_DISP_WIDTH, SETT_TIME_DISP_HEIGHT, GREY_2, "Black Time: ", DEFAULT_FONT, BLACK)
        self.black_time_display.update_time()
        self.white_time_display = Display_Settings_White_Time(0, 0, SETT_TIME_DISP_WIDTH, SETT_TIME_DISP_HEIGHT, GREY_2, "White Time: ", DEFAULT_FONT, BLACK)
        self.white_time_display.update_time()

        self.black_time_inc = Move_Time_Change_Button(0, 0, SETT_TIME_DISP_HEIGHT, SETT_TIME_DISP_HEIGHT, GREY_3, GREY, "+", DEFAULT_FONT, BLACK)
        self.black_time_inc.setup("b+", self.black_time_display)
        self.black_time_dec = Move_Time_Change_Button(0, 0, SETT_TIME_DISP_HEIGHT, SETT_TIME_DISP_HEIGHT, GREY_3, GREY, "-", DEFAULT_FONT, BLACK)
        self.black_time_dec.setup("b-", self.black_time_display)
        self.white_time_inc = Move_Time_Change_Button(0, 0, SETT_TIME_DISP_HEIGHT, SETT_TIME_DISP_HEIGHT, GREY_3, GREY, "+", DEFAULT_FONT, BLACK)
        self.white_time_inc.setup("w+", self.white_time_display)
        self.white_time_dec = Move_Time_Change_Button(0, 0, SETT_TIME_DISP_HEIGHT, SETT_TIME_DISP_HEIGHT, GREY_3, GREY, "-", DEFAULT_FONT, BLACK)
        self.white_time_dec.setup("w-", self.white_time_display)
        self.all_Buttons.extend([self.black_time_inc, self.black_time_dec, self.white_time_inc, self.white_time_dec])

        col1unit1 = [[self.title1], [self.black_time_display, self.black_time_inc, self.black_time_dec], [self.white_time_display, self.white_time_inc, self.white_time_dec]]
        self.col1.append(col1unit1)

    def reset_parameters(self):
        self.black_time_display.update_time()
        self.white_time_display.update_time()

    def set_all_col_positions(self):
        current_y = self.y + SETTINGS_PADDING
        for unit in self.col1:
            for row in unit:
                current_x = self.x + SETTINGS_PADDING
                for elem in row:
                    elem.x = current_x
                    elem.y = current_y
                    current_x += elem.width + SETTINGS_INT_PADDING
                current_y += SETTINGS_INT_PADDING + row[0].height
            current_y += SETTINGS_PADDING

    def draw(self, win):
        pygame.draw.rect(win, GREY_1, (self.x, self.y, SETTINGS_WIDTH, SETTINGS_HEIGHT))
        for button in self.etc_Buttons:
            button.draw(win)
        for unit in self.col1:
            for row in unit:
                for elem in row:
                    elem.draw(win)
    
    def click(self, pos):
        for button in self.all_Buttons:
            if button.is_clicked(pos):
                return button.press()

class Save_Restart_Button(Button):
    def press(self):
        with open(os.path.join('omokFiles', 'settings.json'), 'w') as fp1:
            json.dump(NEW_SETTINGS, fp1, indent = 4)
        pygame.event.post(pygame.event.Event(RESET_EVENT))

class Display_Settings_Black_Time(Display):
    def update_time(self):
        self.drawtext = self.font.render(self.text + str(NEW_SETTINGS["BLACK_TIME_INIT"]), 1, self.font_color)

class Display_Settings_White_Time(Display):
    def update_time(self):
        self.drawtext = self.font.render(self.text + str(NEW_SETTINGS["WHITE_TIME_INIT"]), 1, self.font_color)

class Close_Settings_Button(Button):
    def press(self):
        global NEW_SETTINGS
        NEW_SETTINGS = copy.deepcopy(SETTINGS)
        pygame.event.post(pygame.event.Event(SETTINGS_EVENT))

class Move_Time_Change_Button(Button):
    def setup(self, mode, display):
        self.mode = mode
        self.display = display
    
    def press(self):
        if self.mode == "b+":
            NEW_SETTINGS["BLACK_TIME_INIT"] += 1
        elif self.mode == "b-":
            NEW_SETTINGS["BLACK_TIME_INIT"] -= 1
        elif self.mode == "w+":
            NEW_SETTINGS["WHITE_TIME_INIT"] += 1
        elif self.mode == "w-":
            NEW_SETTINGS["WHITE_TIME_INIT"] -= 1
        self.display.update_time()
