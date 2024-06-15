import pygame
import sys
import os
from config import Config

class MainInterface(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'end_backgrond.png'))
        self.rect = self.image.get_rect()
        self.rect.center = Config.SCREEN_HEIGHT // 2, Config.SCREEN_WIDTH // 2

    def update(self):
        pass

class ContinueButton(pygame.sprite.Sprite):
    def __init__(self, x = Config.SCREEN_WIDTH // 2, y = 400):
        pygame.sprite.Sprite.__init__(self)
        self.image_1 = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'continue_button_1.png'))
        self.image_2 = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'continue_button_2.png'))
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.image_2
        else:
            self.image = self.image_1

class EndInterface():

    def __init__(self):

        self.main_interface = MainInterface()
        self.continue_btn = ContinueButton()
        self.componets = pygame.sprite.LayeredUpdates(self.main_interface, self.continue_btn)

    def update(self, screen):
        clock = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        count = 0
        flag = True
        while True:
            count += 1
            clock.tick(60)
            self.components.clear(screen, background)
            self.components.update()
            if count % 10 == 0:
                count =0
                flag = not flag
            if flag:
                self.components.draw(screen)
            else:
                screen.blit(self.main_interface.image, self.main_interface.rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.continue_btn.rect.collidepoint(mouse_pos):
                            return True