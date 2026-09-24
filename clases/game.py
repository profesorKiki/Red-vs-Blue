import random
from .base_elements import *
from clases.textures import *
from clases.fonts import *
from clases.audio import *

PLAY_GAME = 1
MUTE_GAME = 2
UNMT_GAME = 3
CLIK_BLUE = 4
CLIK__RED = 5
USES_PIKE = 6
SHOW_HELP = 7

TITLE = "RED vs BLUE"
WIN_W = 1280
WIN_H = 720

COLR__RED = 0
COLR_BLUE = 1

MATRX_FIL = 8
MATRX_COL = 8 

BATLEFIEL = pygame.Rect(6,2,13,9)

LEVEL_TIME = 240
PIKES_INIT = 5

TILE_SIZE = 64

class Controller:
    def __init__(self):
        self.timer = None
        self.textures = Textures()
        self.fonts = Fonts()
        self.audio = Audio()
        
        self.game_over = False
        self.wined_red = 0
        self.wined_blu = 0
        
        self.pikes = 0
        self.time = 0

        self.visual = Visual(self.textures, self.fonts)
        self.mboard = MatrixBoard(MATRX_FIL, MATRX_COL)
        

    def mute(self):
        self.audio.mute()        

    def unmute(self):
        self.audio.unmute()
    
    def volume_up(self):
        self.audio.volume_up()

    def volume_down(self):
        self.audio.volume_down()    

    def start(self):
        self.audio.play(GAME_TRAK)
        self.visual.show_help()
                
    def quit(self):
        self.audio.quit()
            
    def draw(self, window):
        self.visual.draw(window.surface)
        #if not self.game_over and self.wined_red != 5 and self.wined_blu != 5:
        #    self.mboard.draw(window.surface)
    
    def clock_time(self):
        self.time-=1
        self.visual.update_time(self.time)
        if not self.time:
            self.visual.show_game_over()
            self.timer.stop()
            self.game_over = True
    
    def start_level(self):
        self.pikes+= PIKES_INIT
        self.time = LEVEL_TIME
        self.mboard.fill_randomized()
        self.visual.create_troops(self.mboard.matrix)
        self.visual.update_time(self.time)
        self.visual.update_pikes(self.pikes)

    def change_troops(self, fil, col):
        self.mboard.change_troop(fil, col)
        self.mboard.change_troop(fil-1, col)
        self.mboard.change_troop(fil+1, col)
        self.mboard.change_troop(fil, col-1)
        self.mboard.change_troop(fil, col+1)
    
    def change_troop(self, fil, col):
        self.mboard.change_troop(fil, col)
    
    def is_completed(self):
        if self.mboard.is_completed():
            if self.mboard.all_red:
                self.wined_red+=1
                self.visual.move_swords_to_blue()
            else:
                self.wined_blu+=1
                self.visual.move_swords_to_red() 
            if self.wined_blu == 5:
                self.visual.winned_blue()
                return
            if self.wined_red == 5:
                self.visual.winned_red()
                return
            self.start_level()
        
    def action(self, event):
        if self.game_over or self.wined_red == 5 or self.wined_blu == 5:
            return Action(EVEN_NONE)

        action = self.visual.action(event)

        if action.id == PLAY_GAME:
            self.start_level()
            self.timer = Timer()
            self.visual.show_game()

        if action.id == USES_PIKE and self.pikes:
            self.pikes-=1
            self.visual.update_pikes(self.pikes)
            self.change_troop(action.data[0], action.data[1])
            self.visual.create_troops(self.mboard.matrix)
            self.is_completed()

        if action.id == CLIK_BLUE or action.id == CLIK__RED:
            self.change_troops(action.data[0], action.data[1])
            self.visual.create_troops(self.mboard.matrix)
            self.is_completed()

        return action    
        

class Visual:
    def __init__(self, textures, font):
        self.background = Background(textures)
        self.hud = Hud(textures, font.get_font(FONT_DFLT)) 
        self.map = Map(textures)
        self.board = Board(textures, BATLEFIEL.x, BATLEFIEL.y)
        self.main = MainTitle(textures, font.get_font(FONT_MAIN))
        self.game_over = GameOver(textures, font.get_font(FONT_MAIN))
        self.blue_victory = Victory(textures, font.get_font(FONT_MAIN))
        self.red_victory = Victory(textures, font.get_font(FONT_MAIN), True)
        self.current = self.main

    def update_pikes(self, pikes):
        self.hud.update_pikes(str(pikes))
    
    def update_time(self, time):
        self.hud.update_time(str(time))
    
    def move_swords_to_blue(self):
        self.map.move_swords_to_blue()
    
    def move_swords_to_red(self):
        self.map.move_swords_to_red()
    
    def winned_blue(self):
        self.current = self.blue_victory
        
    def winned_red(self):
        self.current = self.red_victory

    def create_troops(self, matrix):
        self.board.create_troops(matrix)

    def action(self, event):
        if self.current is None:
            return self.board.action(event)
        return self.current.action(event)
        
    def show_help(self):
        self.current = self.main

    def show_game(self):
        self.current = None    

    def show_game_over(self):
        self.current = self.game_over

    def draw(self,window):
        if self.current is None:
            self.background.draw(window)
            self.hud.draw(window)
            self.map.draw(window)
            self.board.draw(window)
        else:
            self.current.draw(window)    


class Background(Canva):
    def __init__(self, textures):
        super().__init__()
        self.board_fil = 12
        self.board_col = 20
        self._create_grass(textures.sprite(TILE_GRASS, (64, 64)))
        self._create_trees(textures.sprite(TILE_TREES, (64, 64)))
            
    def _create_grass(self, grass_tiles):    
        for i in range(0,self.board_fil):
            grass_index = 1  
            if i % 2:
                grass_index = 0
            for j in range(0,self.board_col):
                self.add_image(grass_tiles[grass_index], j*64, i*64)
                if grass_index == 0:
                    grass_index = 1
                else:
                    grass_index = 0    

    def _create_trees(self, trees_tiles):    
        for fil in range(0,self.board_fil):
            for col in range(0,self.board_col):
                if fil >= BATLEFIEL.y and fil <= BATLEFIEL.h and col >= BATLEFIEL.x and col <= BATLEFIEL.w:
                    continue
                self.add_image(trees_tiles[0], col*64, fil*64)
        

class Hud(Canva):
    def __init__(self, textures, font):
        super().__init__()
        self.add_image(textures.image(IMAG_TITLE))
        self.add_image(textures.image(IMAG_BANE2), 55, 55)
        self.add_image(textures.image(IMAG_BANE2), 55, 95)
        self.add_text("Time:" , font, "black",  60,  60)
        self.add_text("Pikes:", font, "black",  60, 100)
        self.add_text("0"     , font, "black", 160, 100)
        self.add_text("0"     , font, "black", 160,  60)        

    def update_pikes(self, pikes):
        self.set_text(2, pikes)
    
    def update_time(self, time):
        self.set_text(3, time)


class Map(Canva):
    def __init__(self, textures):
        super().__init__()
        self.add_image(textures.image(IMAG_BANER, (508,76))   , 387, 35)
        self.add_image(textures.sprite(TROP__BLUE, (64, 64))[0], 393, 40)
        self.add_image(textures.sprite(TROP___RED, (64, 64))[0], 825, 40)
        self.add_image(textures.image(IMAG__MARK), 622, 55)
        
    def move_swords_to_blue(self):
        self.images[3].rect.x-=44
    
    def move_swords_to_red(self):
        self.images[3].rect.x+=44
    
    
class MatrixBoard:
    def __init__(self, fil=0, col=0):
        self.fil = fil
        self.col = col
        self.matrix = []        
        self.all_red = False
        self.all_blu = False
        self._create()
            
    def _create(self):
        for fil in range(0,self.fil):
            a = [] 
            for col in range(0,self.col):
                a.append(0)
            self.matrix.append(a)
    
    def fill_randomized(self):
        for fil in range(0,self.fil):
            for col in range(0,self.col):
                self.matrix[fil][col]=random.randrange(2)
    
    def change_troop(self, fil, col):
        if fil >= 0 and fil < self.fil and col >= 0 and col < self.col:
            if self.matrix[fil][col]==COLR_BLUE:
                self.matrix[fil][col]=COLR__RED
            else:
                self.matrix[fil][col]=COLR_BLUE
    
    def is_completed(self):
        self.all_red = False
        self.all_blu = False
        for fil in range(len(self.matrix[0])):
            for col in range(len(self.matrix[0])):
                if self.matrix[fil][col]==COLR_BLUE:
                    self.all_blu = True
                else:
                    self.all_red = True
        return self.all_red and not self.all_blu or self.all_blu and not self.all_red                
    
        
class Board(Canva):
    def __init__(self, texture, x, y):
        super().__init__()
        self.x = x 
        self.y = y         
        self.blu = texture.sprite(TROP__BLUE, (TILE_SIZE,TILE_SIZE))
        self.red = texture.sprite(TROP___RED, (TILE_SIZE,TILE_SIZE))
    
    def create_troops(self, matrix):
        self.buttons.clear()               
        for fil in range(len(matrix[0])):
            for col in range(len(matrix[0])):
                if matrix[fil][col]:
                    self.add_button(self.blu, (self.x+col)*TILE_SIZE, (self.y+fil)*TILE_SIZE, Action(CLIK_BLUE, [fil, col]))
                else:
                    self.add_button(self.red, (self.x+col)*TILE_SIZE, (self.y+fil)*TILE_SIZE, Action(CLIK__RED, [fil, col]))                          
    
    def action(self, event):
        action = super().action(event)
        for button in self.buttons:
            if button.detect_mouse_over(pygame.mouse.get_pos()) and event == EVEN_RCLK:
                return Action(USES_PIKE, [ button.action.data[0], button.action.data[1]])
        return action


class MainTitle(Canva):
    def __init__(self, textures, font):
        super().__init__()
        self.add_option("START GAME", font, "black", "yellow",  540, 300, Action(PLAY_GAME))
        self.add_option("HELP", font, "black", "yellow",  20, 655, Action(SHOW_HELP))
    
        self._create_grass(textures.sprite(TILE_GRASS, (64, 64)))
        self._create_trees(textures.sprite(TILE_TREES, (64, 64)))
        
        self.add_image(textures.image(IMAG_BANER,(508,76)), 390, 200)
        self.add_image(textures.image(IMAG_TITLE), 505, 210)
        
        self.help = Help(textures, 120, 640, False)
    
    def _create_grass(self, grass_tiles):    
        for i in range(0,12):
            for j in range(0,20):
                self.add_image(grass_tiles[random.randrange(2)], j*64, i*64)
            
    def _create_trees(self, trees_tiles):    
        for fil in range(0,12):
            for col in range(0,20):
                if random.randrange(2):
                    continue
                self.add_image(trees_tiles[0], col*64, fil*64)    
    
    def draw(self, window):
        super().draw(window)
        self.help.draw(window) 

    def action(self, event):
        action = super().action(event)
        if action.id == SHOW_HELP:
            if self.help.visible:
                self.help.hide()
            else:
                self.help.show()
        return action    


class Help(Form):
    def __init__(self, textures, x=0, y=0, visible="True"):
        super().__init__(x, y, visible)
        self.add_image(textures.image(IMAG_BANER,(508,76)), self.x, self.y)
        self.add_image(textures.image(IMAG_HELPA), self.x +  20, self.y+15)
        self.add_image(textures.image(IMAG_HELPB), self.x + 240, self.y+15)
        self.add_image(textures.image(IMAG_HELPC), self.x + 400, self.y+15)


class GameOver(Canva):
    def __init__(self, textures, font):
        super().__init__()
        self.add_text("GAME OVER", font, "black",  540, 300)
    
        self._create_grass(textures.sprite(TILE_DUSTT, (64, 64)))
        
        self.add_image(textures.image(IMAG_BANER,(508,76)), 390, 200)
        self.add_image(textures.image(IMAG_TITLE), 505, 210)
        
    def _create_grass(self, dust_tiles):    
        for i in range(0,12):
            for j in range(0,20):
                self.add_image(dust_tiles[1], j*64, i*64)
        
        for i in range(0,12):
            for j in range(0,20):
                if random.randrange(100) < 20:
                    self.add_image(dust_tiles[0], j*64, i*64)
            

class Victory(Canva):
    def __init__(self, textures, font, red=False):
        super().__init__()
        
        if red:
            self.add_text("RED WINS", font, "black",  540, 300)
            self._create_grass(textures.sprite(TILE_GRASS, (64, 64)), textures.sprite(TROP___RED, (TILE_SIZE,TILE_SIZE)))
        else:
            self.add_text("BLUE WINS", font, "black",  540, 300)
            self._create_grass(textures.sprite(TILE_GRASS, (64, 64)), textures.sprite(TROP__BLUE, (TILE_SIZE,TILE_SIZE)))
            
        self.add_image(textures.image(IMAG_BANER,(508,76)), 390, 200)
        self.add_image(textures.image(IMAG_TITLE), 505, 210)
        
    def _create_grass(self, grass_tiles, blu):    
        for i in range(0,12):
            for j in range(0,20):
                self.add_image(grass_tiles[1], j*64, i*64)
        
        for i in range(0,12):
            for j in range(0,20):
                if random.randrange(100) < 20:
                    self.add_image(blu[0], j*64, i*64)    