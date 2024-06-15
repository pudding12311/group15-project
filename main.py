import pygame
import sys
import os
from game.config import Config

# 初始化 Pygame
pygame.init()

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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption(Config.SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False
        self.current_warrior = None
        self.warriors = {}
        self.load_warriors()
        self.button_image = pygame.image.load(os.path.join(Config.IMAGE_PATH, 'button.png')).convert_alpha()
        self.button_rect = self.button_image.get_rect(center=(Config.SCREEN_WIDTH // 2, Config.SCREEN_HEIGHT // 2))
        self.game_font = pygame.font.Font(os.path.join(Config.FONT_PATH, 'Mamelon.otf'), 36)

    def load_warriors(self):
        for i in range(1, 3):
            warrior_name = f"warrior_{i}.png"
            self.warriors[i] = Warrior(warrior_name)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    warrior_index = event.key - pygame.K_1 + 1
                    if warrior_index in self.warriors:
                        self.current_warrior = self.warriors[warrior_index]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    self.game_started = True
    def start_screen(self):
        while not self.game_started:
            self.handle_events()
            self.screen.blit(pygame.image.load(os.path.join(Config.IMAGE_PATH, 'test-background.png')).convert(), (0, 0))
            if not self.game_started:
                self.screen.blit(self.button_image, self.button_rect)
            text_surface = self.game_font.render("測試", True, Config.WHITE)
            text_rect = text_surface.get_rect(midtop=(Config.SCREEN_WIDTH // 2, 50))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            self.clock.tick(Config.FPS)

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.screen.fill(Config.BLACK)
            if self.current_warrior:
                self.current_warrior.update()
                self.screen.blit(pygame.image.load(os.path.join(Config.IMAGE_PATH, 'test-background.png')).convert(), (0, 0))
                self.screen.blit(self.current_warrior.image, self.current_warrior.rect)
            pygame.display.flip()
            self.clock.tick(Config.FPS)

    def run(self):
        self.start_screen()
        self.game_loop()

if __name__ == "__main__":
    game = Game()
    game.run()

# 退出 Pygame
pygame.quit()
sys.exit()
