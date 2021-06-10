import pygame
from .utilities import Button, Settings_Button
from .constants import BLACK, BUTTON_PADDING, DEFAULT_FONT, GREEN_1, GREY_1, SETTINGS_BUTTON_HEIGHT, SETTINGS_BUTTON_WIDTH, SETTINGS_HEIGHT, SETTINGS_PADDING, SETTINGS_PADDING, SETTINGS_WIDTH

class Settings():
    def __init__(self):
        self.x, self.y = SETTINGS_PADDING, SETTINGS_PADDING
        self.width, self.height = SETTINGS_WIDTH, SETTINGS_HEIGHT
        self.all_Buttons = []
        self.closeButton = Settings_Button(self.x + self.width - BUTTON_PADDING - SETTINGS_BUTTON_WIDTH, self.y + BUTTON_PADDING, SETTINGS_BUTTON_WIDTH, SETTINGS_BUTTON_HEIGHT, GREEN_1, GREEN_1, "Close", DEFAULT_FONT, BLACK)
        self.all_Buttons.append(self.closeButton)
    
    def draw(self, win):
        pygame.draw.rect(win, GREY_1, (self.x, self.y, SETTINGS_WIDTH, SETTINGS_HEIGHT))
        for button in self.all_Buttons:
            button.draw(win)
    
    def click(self, pos):
        for button in self.all_Buttons:
            if button.is_clicked(pos):
                return button.press()