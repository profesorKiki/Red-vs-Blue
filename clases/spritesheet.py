import pygame

class Spritesheet(object):
    def __init__(self, file):
        self.sheet = pygame.image.load(file)
        self.sheet.convert()
    
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.convert()
        image.blit(self.sheet, (0, 0), rect)
        return image
    
    def image_list(self, rects):
        img_list = []
        for rect in rects:
            img_list.append(self.image_at(rect))
        return img_list
        
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)