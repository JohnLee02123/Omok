import pygame
from .constants import BLACK

class JohnPhaGo:
    def __init__(self):
        pass

    def calcNextMove(self, state):
        if state.turn == BLACK:
            if state.pot_to_square_b['05']:
                nxt = next(iter(state.pot_to_square_b['05']))
                return (nxt, 'b')
            w5l = len(state.pot_to_square_w['05'])
            if w5l > 0:
                nxt = next(iter(state.pot_to_square_w['05']))
                if w5l > 1:
                    return (nxt, 'w')
                return (nxt, '?')
        else:
            if state.pot_to_square_w['05']:
                nxt = next(iter(state.pot_to_square_w['05']))
                return nxt
            b5l = len(state.pot_to_square_b['05'])
            if b5l > 0:
                nxt = next(iter(state.pot_to_square_b['05']))
            elif state.pot_to_square_b['05']:
                nxt = next(iter(state.pot_to_square_b['05']))