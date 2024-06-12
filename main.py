import pygame
import sys
import os
from config import *

# 初始化 Pygame
pygame.init()

# 設定屏幕大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

# 加載圖像並檢查路徑
def load_image(file_name):
    file_path = os.path.join(IMAGE_PATH, file_name)
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        sys.exit()
    return pygame.image.load(file_path)

background_image = load_image('test-background.png')
player_image = load_image('test-player.png')
player_width = 300  # 調整為適當的大小
player_height = 300  # 調整為適當的大小
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# 玩家位置和速度
player_x = 50
player_y = SCREEN_HEIGHT // 2
player_speed = 5
player_direction = 'right'

# 主遊戲循環
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 處理玩家輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_image.get_height():
        player_y += player_speed
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        player_direction = 'left'
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_image.get_width():
        player_x += player_speed
        player_direction = 'right'

    # 繪製背景
    screen.blit(background_image, (0, 0))
    
    # 繪製玩家
    screen.blit(player_image, (player_x, player_y))

    # 更新屏幕
    pygame.display.flip()

    # 控制遊戲速度
    clock.tick(FPS)

# 退出 Pygame
pygame.quit()
sys.exit()
