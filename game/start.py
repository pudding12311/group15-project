import pygame
import os
from config import Config
import sys
sys.path.append('/home/obi/oop-final-game/assets')

class MainInterface(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'start_background.png'))
        self.image = pygame.transform.scale(self.image,(Config.SCREEN_WIDTH,Config.SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = 640, 360

    def update(self):
        pass

class PlayButton(pygame.sprite.Sprite):
    def __init__(self, x = 850, y = 480):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'play_button1.png'))
        self.image_2 = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'play_button2.png'))
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_2
        else:
            self.image = self.image_1

class StartInterface():

    def __init__(self):

        self.main_interface = MainInterface()
        self.play_btn = PlayButton()
        self.componets = pygame.sprite.LayeredUpdates(self.main_interface, self.play_btn)

    def update(self, screen):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.componets.update()
            self.componets.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_btn.rect.collidepoint(mouse_pos):
                            return True