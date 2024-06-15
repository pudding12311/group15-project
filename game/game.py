import pygame
import sys
import os
from config import Config

# 初始化 Pygame
pygame.init()

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_caption(Config.SCREEN_TITLE)

class Warrior(pygame.sprite.Sprite):
    def __init__(self, warrior_name):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Config.IMAGE_PATH, warrior_name)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (Config.SCREEN_WIDTH // 4, Config.SCREEN_HEIGHT // 2)  # 从屏幕中间左侧开始
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > Config.SCREEN_WIDTH:  # 如果战士移出屏幕右侧，重新从左侧开始
            self.rect.right = 0

all_sprites = pygame.sprite.Group()
warrior = Warrior()


while running:
    clock.tick(Config.FPS)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(Config.WHITE)
    pygame.display.update()

pygame.quit()
sys.exit()
    