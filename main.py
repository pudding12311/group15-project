import pygame
import sys
sys.path.append('/home/obi/oop-final-game/game')
from game.config import *
from game.start import *
from game.game import *
from game.pause import *
from game.end import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption(Config.SCREEN_TITLE)
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(Config.SOUND_PATH, "music.mp3"))
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.25)

    start_interface = StartInterface()
    is_play = start_interface.update(screen)
    if not is_play:
        return
    
    while True:
        game_interface = GameInterface(screen)
        game_interface.start()
        end_interface = EndInterface()
        end_interface.update(screen)

if __name__ == '__main__':
    main()

