import pygame

class Window():
    def __init__(self, title, w, h, color="gray8"):
        pygame.display.set_caption(title)
        self.surface = pygame.display.set_mode((w, h))
        self.surface.fill(pygame.Color(color))
        