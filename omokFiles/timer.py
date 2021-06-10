import pygame
import time
from .utilities import Button
from .constants import BLACK, BLACK_TIME_INIT, DEFAULT_FONT, TIMER_BORDER_COLOR, TIMER_BORDER_THICKNESS, TIMER_COLOR, TIMER_HEIGHT, TIMER_WIDTH, TIMER_X, TIMER_X, TIMER_Y, WHITE, WHITE_TIME_INIT

class Timer:
    def __init__(self):
        self.x = TIMER_X
        self.y = TIMER_Y
        self.border_color = TIMER_BORDER_COLOR
        self.color = TIMER_COLOR
        self.height = TIMER_HEIGHT
        self.width = TIMER_WIDTH
        self.font = pygame.font.SysFont(DEFAULT_FONT, self.height // 10 * 10)
        self.font_color = BLACK
        self.blackTime = BLACK_TIME_INIT
        self.whiteTime = WHITE_TIME_INIT
        self.text = '0'
        self.drawtext = self.font.render(self.text, 1, self.font_color)
        self.text_x = self.x + self.width // 2 - self.drawtext.get_width() // 2
        self.text_y = self.y + self.height // 2 - self.drawtext.get_height() // 2
        self.turn = 1
        self.startTime = time.time()
        self.started = True
    
    def calculate_text_pos(self):
        self.text_x = self.x + self.width // 2 - self.drawtext.get_width() // 2
        self.text_y = self.y + self.height // 2 - self.drawtext.get_height() // 2

    def start(self):
        self.startTime = time.time()
        self.started = True

    def change_turn(self):
        self.turn *= -1
        self.startTime = time.time()

    def draw(self, win):
        pygame.draw.rect(win, self.border_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.color, (self.x + TIMER_BORDER_THICKNESS, self.y + TIMER_BORDER_THICKNESS, self.width - TIMER_BORDER_THICKNESS * 2, self.height - TIMER_BORDER_THICKNESS * 2))
        pygame.draw.rect(win, self.border_color, (self.x + self.width // 2 - TIMER_BORDER_THICKNESS // 2, self.y, TIMER_BORDER_THICKNESS, self.height))
        white_current = self.whiteTime
        black_current = self.blackTime
        if self.started == False:
            pass
        elif self.turn == 1:
            black_current = max(self.blackTime - (time.time() - self.startTime), 0)
        else:
            white_current = max(self.whiteTime - (time.time() - self.startTime), 0)
        black_render = self.font.render("{:.1f}".format(black_current), 1, BLACK)
        white_render = self.font.render("{:.1f}".format(white_current), 1, WHITE)
        win.blit(black_render, (self.x + self.width // 4 - black_render.get_width() // 2, self.y + self.height // 2 - black_render.get_height() // 2))
        win.blit(white_render, (self.x + self.width // 4 * 3 - white_render.get_width() // 2, self.y + self.height // 2 - white_render.get_height() // 2))

    def is_clicked(self, pos):
        px, py = pos
        if px > self.x and px <= self.x + self.width and py > self.y and py <= self.y + self.height:
            return True
        return False