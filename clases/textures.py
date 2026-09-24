from clases.spritesheet import *

TILE_GRASS = 0
TILE_TREES = 1
TROP__BLUE = 2
TROP___RED = 3
TILE_DUSTT = 4

IMAG_TITLE = 0
IMAG_BANER = 1
IMAG__MARK = 2
IMAG_BANE2 = 3
IMAG_HELPA = 4
IMAG_HELPB = 5
IMAG_HELPC = 6


class Textures:
    def __init__(self):
        self.texture = Spritesheet("img/Tiles.png")
        self.sprites = []
        self.sprites.append(self.texture.image_list([(32, 0, 16, 16),(32, 16, 16, 16)]))    #TILE_GRASS
        self.sprites.append(self.texture.image_list([(16, 16, 16, 16)]))                    #TILE_TREES
        self.sprites.append(self.texture.image_list([(0, 0, 16, 16), (0, 32, 16, 16)]))     #TROP__BLUE
        self.sprites.append(self.texture.image_list([(16, 0, 16, 16),(16, 32, 16, 16)]))    #TROP___RED
        self.sprites.append(self.texture.image_list([(32, 32, 16, 16),(32, 48, 16, 16)]))   #TILE_DUSTT
        
        self.images = []
        self.images.append(pygame.image.load("img/Title.png").convert_alpha())       #IMAG_TITLE
        self.images.append(pygame.image.load("img/Banner.png").convert_alpha())      #IMAG_BANER
        self.images.append(pygame.image.load("img/Marca.png").convert_alpha())       #IMAG__MARK
        self.images.append(pygame.image.load("img/Banner_2.png").convert_alpha())    #IMAG_BANE2
        self.images.append(pygame.image.load("img/help_a.png").convert_alpha())      #IMAG_HELPA
        self.images.append(pygame.image.load("img/help_b.png").convert_alpha())      #IMAG_HELPB
        self.images.append(pygame.image.load("img/help_c.png").convert_alpha())      #IMAG_HELPC

        
                                                

    def sprite(self, sprite_index, scale = None):
        if scale is None:
            return self.sprites[sprite_index]
        
        sprites_scaled = []
        for sprite in self.sprites[sprite_index]:
            sprites_scaled.append(pygame.transform.scale(sprite,scale))
        
        return sprites_scaled            

    def image(self, image_index, scale=None):
        if scale is None:
            return self.images[image_index]
        return pygame.transform.scale(self.images[image_index], scale)
        