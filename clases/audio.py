import pygame

GAME_TRAK = 0

class Audio:
    def __init__(self):
        pygame.mixer.get_init()
        pygame.mixer.get_num_channels()
        self.tracks = []
        self.tracks.append(pygame.mixer.Sound('snd/time_to_puzzle.ogg'))
        self.current_track = 0
        self.volume = 0.5
        self._set_volume()

    def play(self,track_index,loop=-1):
        self.current_track = track_index
        self.tracks[self.current_track].play(loop)

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()    

    def stop(self):
        pygame.mixer.stop()

    def mute(self):
        self.tracks[self.current_track].set_volume(0.0)

    def unmute(self):
        self.tracks[self.current_track].set_volume(1.0)

    def _set_volume(self):
        self.tracks[self.current_track].set_volume(self.volume)

    def volume_up(self):
        self.volume+=0.1
        if self.volume > 1.0:
            self.volume = 1.0
        self._set_volume()    

    def volume_down(self):
        self.volume-=0.1
        if self.volume < 0.0:
            self.volume = 0.0
        self._set_volume()    


    def quit(self):
        pygame.mixer.quit()    
      
