import pygame

EVEN_NONE = 0 #Not Keyboard or Mouse events detected
EVEN_QUIT = 1 #Close Window
EVEN_LCLK = 2 #Left Click
EVEN_RCLK = 3 #Right Click
EVEN_CLOK = 4 #Timeout
EVEN_WHDW = 5 #Mouse Wheel Down
EVEN_WHUP = 6 #Mouse Wheel Up

EVEN_TIME = pygame.USEREVENT + 1 #Revisar para soportar varios timers

class Input:
    def detect(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return EVEN_QUIT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return EVEN_LCLK    
                if pygame.mouse.get_pressed()[2]:
                    return EVEN_RCLK
                if event.button == 5:
                    return EVEN_WHDW
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    return EVEN_WHUP    
            
            if event.type == EVEN_TIME:
                return EVEN_CLOK         
        
        return EVEN_NONE

class Timer:
    def __init__(self, time=1000, loop=0):
        pygame.time.set_timer(EVEN_TIME, time, loop)                
    
    def stop(self):
        pygame.time.set_timer(EVEN_TIME, 0)                
    