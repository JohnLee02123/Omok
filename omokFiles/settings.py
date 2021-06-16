import pygame
import os
import json
import copy
from .utilities import Button, Settings_Button
from .constants import BLACK, BUTTON_PADDING, DEFAULT_FONT, GREEN_1, GREEN_2, GREY_1, NEW_SETTINGS, RESET_EVENT, SAVE_RESTART_BUTTON_HEIGHT, SAVE_RESTART_BUTTON_WIDTH, SETTINGS, SETTINGS_BUTTON_HEIGHT, SETTINGS_BUTTON_WIDTH, SETTINGS_HEIGHT, SETTINGS_PADDING, SETTINGS_PADDING, SETTINGS_WIDTH

class Settings():
    def __init__(self):
        self.x, self.y = SETTINGS_PADDING, SETTINGS_PADDING
        self.width, self.height = SETTINGS_WIDTH, SETTINGS_HEIGHT
        self.changed = False
        self.all_Buttons = []
        self.closeButton = Settings_Button(self.x + self.width - BUTTON_PADDING - SETTINGS_BUTTON_WIDTH, self.y + BUTTON_PADDING, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT, GREEN_1, GREEN_1, "Close", DEFAULT_FONT, BLACK)
        self.save_restart_button = Save_Restart_Button(self.x + self.width - BUTTON_PADDING - SAVE_RESTART_BUTTON_WIDTH, self.y + self.height - BUTTON_PADDING - SAVE_RESTART_BUTTON_HEIGHT, SAVE_RESTART_BUTTON_WIDTH, SAVE_RESTART_BUTTON_HEIGHT, GREEN_2, GREEN_2, "Save and Restart", DEFAULT_FONT, BLACK)
        self.all_Buttons.append(self.closeButton)
        self.all_Buttons.append(self.save_restart_button)
    
    def draw(self, win):
        pygame.draw.rect(win, GREY_1, (self.x, self.y, SETTINGS_WIDTH, SETTINGS_HEIGHT))
        for button in self.all_Buttons:
            button.draw(win)
    
    def click(self, pos):
        for button in self.all_Buttons:
            if button.is_clicked(pos):
                return button.press()

class Save_Restart_Button(Button):
    def press(self):
        with open(os.path.join('omokFiles', 'settings.json'), 'w') as fp1:
            json.dump(NEW_SETTINGS, fp1, indent = 4)
        SETTINGS = copy.deepcopy(NEW_SETTINGS)
        pygame.event.post(pygame.event.Event(RESET_EVENT))
