from clases.game import *
from clases.window import Window

class Game:
    def __init__(self, fps=60):
        pygame.init()        
        self.window = Window(TITLE, WIN_W, WIN_H)
        self.input = Input()         
        self.game = Controller()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False        
        
    def run(self):
        self.game.start()
        self.running = True
        while self.running:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.fps)
        self.game.quit()
        pygame.quit()

    def _check_events(self):
        event = self.input.detect()
        if event == EVEN_QUIT:
            self.running = False
        if event == EVEN_WHUP:
            self.game.volume_up()
        if event == EVEN_WHDW:
            self.game.volume_down()
        if event == EVEN_CLOK:
            self.game.clock_time()
        self.game.action(event)    

    def _update_screen(self):
        self.game.draw(self.window)
        pygame.display.update()         
    

if __name__ == "__main__":
    game = Game()
    game.run()