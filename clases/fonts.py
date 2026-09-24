import pygame

FONT_DFLT = 0
FONT_MAIN = 1

class Fonts:
    def __init__(self):
        self.fonts = []
        self.fonts.append(pygame.font.SysFont("carlito", 30, bold=True))
        self.fonts.append(pygame.font.SysFont("8bitoperator", 28, bold=True))
        
    def get_font(self,font_index):
        return self.fonts[font_index]
