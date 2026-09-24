from clases.input import *

class Action:
    def __init__(self, id, data=[]):
        self.id = id 
        self.data = data

class Element():
    def __init__(self, x=0, y=0, w=0, h=0, color="white", visible=True):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color(color)
        self.visible = visible    
    
    def detect_collision(self, pos):
        if self.visible:
            return self.rect.collidepoint(pos)
    
    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def set_color_by_rgb(self,color):
        self.color = color          
    
    def set_color_by_name(self,name):
        self.color = pygame.Color(name)
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_dimension(self, w, h): 
        self.rect.w = w
        self.rect.h = h
        
    def draw(self,window, surface):
        if self.visible:
            window.blit(surface, self.get_position())
    

class Text(Element):
    def __init__(self, text, font, color, x, y, antialias = 1, visible = True):
        super().__init__(x, y, 0, 0, color, visible)
        self.font = font
        self.antialias = antialias
        self.set_text(text)

    def set_color_by_rgb(self,color):
        super().set_color_by_rgb(color)
        self.surface = self.font.render(self.text, self.antialias, self.color)
    
    def set_color_by_name(self,name):
        super().set_color_by_name(name)
        self.surface = self.font.render(self.text, self.antialias, self.color)

    def set_text(self,text):
        self.text = text
        self.surface = self.font.render(self.text, self.antialias, self.color)
        super().set_dimension(self.surface.get_width(), self.surface.get_height())
    
    def draw(self,window):
        super().draw(window, self.surface)
        

class TextOption(Text):
    def __init__(self, text, font, color, over_color, x, y, action, antialias=1, visible=True):
        super().__init__(text, font, color, x, y, antialias, visible)
        self.over_color = pygame.Color(over_color)
        self.action = action

    def detect_mouse_over(self, pos):
        if self.detect_collision(pos):
            self.surface = self.font.render(self.text, self.antialias, pygame.Color(self.over_color))
            return True
        self.surface = self.font.render(self.text, self.antialias, pygame.Color(self.color))
        return False

    def set_over_color_by_name(self,color):
        self.over_color = pygame.Color(color)
        self.surface = self.font.render(self.text, 1, self.color)


class Image(Element):
    def __init__(self, image, x, y, color="white", visible=True):
        super().__init__(x, y, 0, 0, color, visible)
        self.image = image
        self.set_dimension(self.image.get_width(), self.image.get_height())
    
    def draw(self,window):
        super().draw(window, self.image)
        

class Button(Element):
    def __init__(self, images, x, y, action, color="white", visible="True"):
        super().__init__(x, y, images[0].get_width(), images[0].get_height(), color, visible)
        self.images = images
        self.curren = images[0]
        self.action = action

    def draw(self,window):
        super().draw(window,self.curren)
    
    def detect_mouse_over(self, pos):
        if self.detect_collision(pos):
            self.curren = self.images[1]
            return True
        self.curren = self.images[0]
        return False     

class Canva:
    def __init__(self):
        self.images = []
        self.options = []
        self.texts = []
        self.buttons = []        
    
    def add_image(self, image, x=0, y=0):
        self.images.append(Image(image, x, y))

    def add_option(self, text, font, base_color, over_color, x, y, action):
        self.options.append(TextOption(text, font, base_color, over_color, x, y, action))

    def add_text(self, text, font, base_color, x, y, antialias=1):
        self.texts.append(Text(text, font, base_color, x, y, antialias))
    
    def add_button(self, images, x, y, action):
        self.buttons.append(Button(images, x, y, action))
    
    def set_text(self, index, text):
        self.texts[index].set_text(text)    
    
    def action(self, event):
        for option in self.options:
            if option.detect_mouse_over(pygame.mouse.get_pos()) and event == EVEN_LCLK:
                return option.action  
        for button in self.buttons:
            if button.detect_mouse_over(pygame.mouse.get_pos()) and event == EVEN_LCLK:
                return button.action
        return Action(EVEN_NONE)     

    def draw(self,window):
        for image in self.images:
            image.draw(window) 
        for option in self.options:
            option.draw(window) 
        for text in self.texts:
            text.draw(window) 
        for button in self.buttons:
            button.draw(window)

class Form(Canva):
    def __init__(self, x=0, y=0, visible="True"):
        super().__init__()
        self.x = x
        self.y = y
        self.visible = visible 

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True 

    def draw(self,window):        
        if self.visible:
            super().draw(window)