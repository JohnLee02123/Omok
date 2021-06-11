import pygame
from .constants import BUTTON_INT_PADDING, BUTTON_PADDING, CONSOLE_HEIGHT, CONSOLE_LEFT_PADDING, CONSOLE_LENGTH, CONSOLE_TEXT_FONT, DEFAULT_FONT, DRAW_B_POT, DRAW_N_POT, DRAW_W_POT, GREY_1, GREY_3, GREY_5, PANEL_FONT_SIZE, PANEL_LEFT_PADDING, PANEL_TOP_PADDING, BOARD_LENGTH, BOARD_SIDE_PADDING, BOARD_TOP_PADDING, POTENTIAL_B_HEIGHT, POTENTIAL_B_WIDTH, RESET_B_HEIGHT, RESET_B_WIDTH, RESET_EVENT, SETTINGS_EVENT, UNREDO_BUTTON_HEIGHT, UNREDO_BUTTON_WIDTH, WHITE, BLACK, PANEL_LENGTH, PANEL_HEIGHT, SQUARE_SIZE, PANEL_INT_PADD, PANEL_FONT

class Panel:
    def __init__(self):
        self.x = BOARD_LENGTH + BOARD_SIDE_PADDING + PANEL_LEFT_PADDING
        self.y = BOARD_TOP_PADDING + SQUARE_SIZE//2
    
    def draw(self, win, turn, move_num):
        pygame.draw.rect(win, WHITE, (self.x, self.y, PANEL_LENGTH, PANEL_HEIGHT))
        if turn == BLACK:
            turn = 'Black'
        else:
            turn = 'White'
        turntext = PANEL_FONT.render("Turn: " + turn, 1, BLACK)
        win.blit(turntext, (self.x + PANEL_INT_PADD, self.y + PANEL_INT_PADD))
        move_num_text = PANEL_FONT.render("No. of moves: " + str(move_num), 1, BLACK)
        win.blit(move_num_text, (self.x + PANEL_INT_PADD, self.y + PANEL_INT_PADD + PANEL_FONT_SIZE))

class Console:
    def __init__(self):
        self.x = BOARD_LENGTH + BOARD_SIDE_PADDING + CONSOLE_LEFT_PADDING
        self.y = BOARD_TOP_PADDING + BOARD_LENGTH - CONSOLE_HEIGHT - SQUARE_SIZE//2
        self.etc_buttons = []
        self.left_text = []
        self.left_text_pos = []
        self.left_buttons = []

        self.initialize_buttons()

        self.calculate_button_positions()
    
    def initialize_buttons(self):
        self.reset_button = Reset_Button(self.x + CONSOLE_LENGTH - BUTTON_PADDING - RESET_B_WIDTH, self.y + BUTTON_PADDING, RESET_B_WIDTH, RESET_B_HEIGHT, GREY_3, GREY_5, "Reset", DEFAULT_FONT, BLACK)
        self.etc_buttons.append(self.reset_button)

        self.left_text.append(CONSOLE_TEXT_FONT.render("Potential Display Options", 1, BLACK))
        
        self.pot_n_button = Potential_Button(0, 0, POTENTIAL_B_WIDTH, POTENTIAL_B_HEIGHT, GREY_3, GREY_5, "None", DEFAULT_FONT, BLACK, DRAW_N_POT)
        self.pot_b_button = Potential_Button(0, 0, POTENTIAL_B_WIDTH, POTENTIAL_B_HEIGHT, GREY_3, GREY_5, "Black", DEFAULT_FONT, BLACK, DRAW_B_POT)
        self.pot_w_button = Potential_Button(0, 0, POTENTIAL_B_WIDTH, POTENTIAL_B_HEIGHT, GREY_3, GREY_5, "White", DEFAULT_FONT, BLACK, DRAW_W_POT)
        self.pot_n_button.pressed = True
        self.pot_n_button.partners = [self.pot_b_button, self.pot_w_button]
        self.pot_b_button.partners = [self.pot_n_button, self.pot_w_button]
        self.pot_w_button.partners = [self.pot_n_button, self.pot_b_button]
        self.left_buttons.append([self.pot_n_button, self.pot_b_button, self.pot_w_button])

        self.left_text.append(CONSOLE_TEXT_FONT.render("Game Control", 1, BLACK))
        self.undo_button = Undo_Button(0, 0, UNREDO_BUTTON_WIDTH, UNREDO_BUTTON_HEIGHT, GREY_3, GREY_5, "Undo", DEFAULT_FONT, BLACK)
        self.redo_button = Redo_Button(0, 0, UNREDO_BUTTON_WIDTH, UNREDO_BUTTON_HEIGHT, GREY_3, GREY_5, "Redo", DEFAULT_FONT, BLACK)
        self.left_buttons.append([self.undo_button, self.redo_button])

    def calculate_button_positions(self):
        current_y = self.y + BUTTON_PADDING
        for a in range(len(self.left_text)):
            current_x = self.x + BUTTON_PADDING
            self.left_text_pos.append((current_x, current_y))
            current_y += self.left_text[a].get_height() + BUTTON_INT_PADDING
            maxheight = 0
            for b in range(len(self.left_buttons[a])):
                self.left_buttons[a][b].x = current_x
                self.left_buttons[a][b].y = current_y
                self.left_buttons[a][b].calculate_text_pos()
                current_x += self.left_buttons[a][b].width + BUTTON_INT_PADDING
                maxheight = max(maxheight, self.left_buttons[a][b].height)
            current_y += maxheight + BUTTON_INT_PADDING

    def draw(self, win):
        pygame.draw.rect(win, GREY_1, (self.x, self.y, CONSOLE_LENGTH, CONSOLE_HEIGHT))
        for row in self.left_buttons:
            for button in row:
                button.draw(win)
        for a in range(len(self.left_text)):
            win.blit(self.left_text[a], self.left_text_pos[a])
        for button in self.etc_buttons:
            button.draw(win)
    
    def click(self, pos):
        for button in self.etc_buttons:
            if button.is_clicked(pos):
                return button.press()
        for row in self.left_buttons:
            for button in row:
                if button.is_clicked(pos):
                    return button.press()

class Button:
    def __init__(self, x, y, width, height, color, pressed_color, text, font, font_color):
        self.x = x
        self.y = y
        self.color = color
        self.pressed_color = pressed_color
        self.text = text
        self.height = height
        self.width = width
        self.font = pygame.font.SysFont(font, height // 10 * 6)
        self.font_color = font_color
        self.pressed = False
        self.drawtext = self.font.render(self.text, 1, self.font_color)
        self.text_x = self.x + self.width // 2 - self.drawtext.get_width() // 2
        self.text_y = self.y + self.height // 2 - self.drawtext.get_height() // 2
    
    def calculate_text_pos(self):
        self.text_x = self.x + self.width // 2 - self.drawtext.get_width() // 2
        self.text_y = self.y + self.height // 2 - self.drawtext.get_height() // 2

    def press(self):
        self.pressed = True if self.pressed == False else False
    
    def unpress(self):
        self.pressed = False

    def draw(self, win):
        if self.pressed:
            draw_color = self.pressed_color
        else:
            draw_color = self.color
        pygame.draw.rect(win, draw_color, (self.x, self.y, self.width, self.height))
        win.blit(self.drawtext, (self.text_x, self.text_y))

    def is_clicked(self, pos):
        px, py = pos
        if px > self.x and px <= self.x + self.width and py > self.y and py <= self.y + self.height:
            return True
        return False


class Reset_Button(Button):
    def __init__(self, x, y, width, height, color, pressed_color, text, font, font_color):
        Button.__init__(self, x, y, width, height, color, pressed_color, text, font, font_color)
    
    def press(self):
        super().press()
        pygame.event.post(pygame.event.Event(RESET_EVENT))

class Potential_Button(Button):
    def __init__(self, x, y, width, height, color, pressed_color, text, font, font_color, type):
        Button.__init__(self, x, y, width, height, color, pressed_color, text, font, font_color)
        self.partners = []
        self.type = type # DRAW_B_POT, etc
    
    def press(self):
        if self.pressed:
            return None
        super().press()
        for button in self.partners:
            button.unpress()
        
        return self.type
    
    def ind_press(self):
        super().press()

class Settings_Button(Button):
    def press(self):
        pygame.event.post(pygame.event.Event(SETTINGS_EVENT))

class Undo_Button(Button):
    def press(self):
        return ("undo")

class Redo_Button(Button):
    def press(self):
        return ("redo")