import pygame
import time
import random
import sys
import os
from config import Config

kill_left = 0
kill_right = 0

class GameInterface:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(os.path.join(Config.IMAGE_PATH, "background.png")).convert()
        self.left_castle = Castle(0, Config.SCREEN_HEIGHT - 410, False)
        self.right_castle = Castle(Config.SCREEN_WIDTH - Config.CASTLE_SIZE, Config.SCREEN_HEIGHT - 410, True)
        self.money_system_right = MoneySystem(x = Config.SCREEN_WIDTH - 50)
        self.money_system_left = MoneySystem(x = 50)
        self.game_environment = pygame.sprite.Group()  # Initialize game environment to store characters
        self.projectiles = pygame.sprite.Group()
        

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.left_castle.draw(self.screen)
        self.right_castle.draw(self.screen)
        self.money_system_right.draw(self.screen)
        self.money_system_left.draw(self.screen)
        for character in self.game_environment:
            character.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)

    def update(self):
        self.money_system_right.update()
        self.money_system_left.update()

        for character in self.game_environment:
            if isinstance(character, Character):
                target = self.right_castle if character.direction == 'right' else self.left_castle
            for other_character in self.game_environment:
                if isinstance(other_character, Character) and other_character != character and other_character.direction != character.direction:
                    if abs(character.rect.centerx - other_character.rect.centerx) <= character.stop_distance:
                        target = other_character
        
            character.update(self.screen, target)
            if character.is_attacking:
                projectile = character.shoot()  # Assuming shoot() method returns the projectile
                if projectile:
                    self.projectiles.add(projectile)
        
        self.projectiles.update()

        
        # 檢查城堡的生命值，如果其中一個城堡的生命值小於等於 0，返回 False 以結束遊戲循環
        if self.left_castle.health <= 0 or self.right_castle.health <= 0:
            return False
        return True

    def start(self):
        clock = pygame.time.Clock()
        warriors_left = {'1': (WarriorA, 200), '2': (WarriorB, 300), '3': (WarriorC, 400), '4': (WarriorD, 600)}
        warriors_right = {'up': (WarriorA, 200), 'down': (WarriorB, 300), 'left': (WarriorC, 400), 'right': (WarriorD, 600)}
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    # 在左側城堡前召喚戰士
                    elif event.unicode in warriors_left:
                        warrior_class, cost = warriors_left[event.unicode]
                        if self.money_system_left.spend_money(cost):
                            start_position = 100
                            direction = 'right'
                            warrior = warrior_class(start_position=start_position, direction=direction)
                            self.game_environment.add(warrior)

                    # 在右側城堡前召喚戰士
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if event.key == pygame.K_UP:
                            warrior_class, cost = warriors_right['up']
                        elif event.key == pygame.K_DOWN:
                            warrior_class, cost = warriors_right['down']
                        elif event.key == pygame.K_LEFT:
                            warrior_class, cost = warriors_right['left']
                        elif event.key == pygame.K_RIGHT:
                            warrior_class, cost = warriors_right['right']
                        
                        if self.money_system_right.spend_money(cost):
                            start_position = Config.SCREEN_WIDTH - 200
                            direction = 'left'
                            warrior = warrior_class(start_position=start_position, direction=direction)
                            self.game_environment.add(warrior)
                        
            
            # 更新遊戲狀態，並檢查是否需要結束遊戲
            if not self.update():
                break
            
            # 繪製遊戲畫面
            self.draw()
            
            pygame.display.flip()
            clock.tick(Config.FPS)

class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Config.IMAGE_PATH, "castle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Config.CASTLE_SIZE, Config.CASTLE_SIZE))
        if flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 1000
        self.position = x

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_bar_width = self.rect.width - 40
        health_bar_height = 10
        health_ratio = self.health / 1000
        current_health_bar_width = int(health_bar_width * health_ratio)
        
        health_bar_bg = pygame.Rect(self.rect.x + 20, self.rect.y - 20, health_bar_width, health_bar_height)
        current_health_bar = pygame.Rect(self.rect.x + 20, self.rect.y - 20, current_health_bar_width, health_bar_height)
        
        pygame.draw.rect(screen, (255, 0, 0), health_bar_bg)
        pygame.draw.rect(screen, (0, 255, 0), current_health_bar)

    def update(self):
        pass  # Override if needed for sprite-based updates

class MoneySystem:
    def __init__(self, x):
        self.money = 1000
        self.font = pygame.font.Font(os.path.join(Config.FONT_PATH, 'Mamelon.otf'), 48)
        self.x = x
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        if elapsed_time > 1000:  # If more than a second has passed
            self.last_update_time = current_time
            elapsed_time = 0

        increment_amount = (elapsed_time / 1000) * 50
        self.money += increment_amount

        if self.money % 100 < increment_amount:
            self.money = (self.money // 50) * 50  # Round up to the nearest 100

        self.last_update_time += elapsed_time

    def draw(self, screen):
        money_text = self.font.render(f"{int(self.money)}", True, Config.BLUE)
        money_rect = money_text.get_rect(center=(self.x, Config.SCREEN_HEIGHT - 30))
        screen.blit(money_text, money_rect.topleft)

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False

class Character(pygame.sprite.Sprite):
    def __init__(self, move_image_path, attack_image_path, attack_power, attack_time, attack_interval, is_single_target, attack_range, health, stop_distance, speed, start_position, direction):
        super().__init__()
        self.move_image_path = move_image_path
        self.attack_image_path = attack_image_path
        self.attack_power = attack_power
        self.attack_time = attack_time
        self.attack_interval = attack_interval
        self.is_single_target = is_single_target
        self.attack_range = attack_range if not is_single_target else None
        self.health = health
        self.stop_distance = stop_distance
        self.speed = speed
        self.position = start_position
        self.direction = direction
        self.last_attack_time = 0
        self.is_attacking = False
        self.rect = None
        self.flipped = direction
        self.load_images(move_image_path, attack_image_path)

    def load_images(self, move_image_path, attack_image_path):
        self.move_image = pygame.image.load(move_image_path).convert_alpha()
        self.move_image = pygame.transform.scale(self.move_image,(Config.WARRIOR_SIZE, Config.WARRIOR_SIZE))
        self.attack_image = pygame.image.load(attack_image_path).convert_alpha()
        self.attack_image = pygame.transform.scale(self.attack_image,(Config.WARRIOR_SIZE, Config.WARRIOR_SIZE))

        if self.flipped == 'left':
            self.move_image = pygame.transform.flip(self.move_image, True, False)
            self.attack_image = pygame.transform.flip(self.attack_image, True, False)

        self.image = self.move_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position, 400 + random.randint(-10, 10))


    def move(self):
        if self.direction == 'right':
            self.position += self.speed
        else:
            self.position -= self.speed
        self.rect.x = self.position

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Remove this sprite from all groups
            if self.direction == 'left':
                kill_left += 1
            else:
                kill_right += 1
    
    def shoot(self):
        # Implement shoot method to create and return a projectile
        # Example implementation:
        if self.is_attacking:
            projectile = Projectile(self.rect.center, self.direction, self.stop_distance)
            return projectile
        return None

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Adjust the y-position as needed

    def update(self):
        pass

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_position, direction, stop_distance):
        super().__init__()
        
        self.direction = direction  # 'left' or 'right'
        self.speed = 5  # Adjust speed as needed
        self.stop_distance = stop_distance
        self.start_position = start_position
        self.distance_traveled = 0
        self.load_images()
        self.rect = self.image.get_rect(center= (start_position[0] +10,start_position[1] - 25))

    def load_images(self):
        self.image = pygame.image.load(os.path.join(Config.IMAGE_PATH, "warrior_b2_bird.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image,(60, 60))
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
 

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed

        self.distance_traveled += self.speed

        # Check if projectile reaches stop distance
        if abs(self.distance_traveled - self.start_position[0]) >= self.stop_distance:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class WarriorA(Character):
    def __init__(self, start_position, direction):
        super().__init__(
            move_image_path = os.path.join(Config.IMAGE_PATH, "warrior_a1.png"), 
            attack_image_path = os.path.join(Config.IMAGE_PATH, "warrior_a2.png"), 
            attack_power = random.randint(30, 60), 
            attack_time = 0.5, 
            attack_interval = 1, 
            is_single_target = True, 
            attack_range = None, 
            health = 250, 
            stop_distance = Config.WARRIOR_SIZE // 2, 
            speed = 2, 
            start_position=start_position, 
            direction=direction
        )

    def attack(self, target):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            attack_power = random.randint(10, 30)  # Random attack power between 10 and 30
            self.image = self.attack_image
            target.take_damage(attack_power)
            self.is_attacking = True
            self.last_attack_time = current_time
        elif current_time - self.last_attack_time >= self.attack_time:
            self.image = self.move_image
        


    def update(self, screen, targets):
        if isinstance(targets, Character):
            # 如果目标是战士且方向与自己不同，进行攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
                
        elif isinstance(targets, Castle):
            # 如果目标是城堡，直接攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
        
        self.draw(screen)

class WarriorB(Character):
    def __init__(self, start_position, direction):
        super().__init__(
            move_image_path = os.path.join(Config.IMAGE_PATH, "warrior_b1.png"), 
            attack_image_path = os.path.join(Config.IMAGE_PATH, "warrior_b2.png"), 
            attack_power = random.randint(40, 60), 
            attack_time = 1.5, 
            attack_interval = 1.5, 
            is_single_target = True, 
            attack_range = None, 
            health = 150, 
            stop_distance = Config.WARRIOR_SIZE + 150, 
            speed = 3, 
            start_position=start_position, 
            direction=direction
        )        
        self.projectile = None
        self.is_attacking = False
        self.attack_start_time = 0

    def attack(self, target):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            attack_power = random.randint(20, 30)  # Random attack power between 10 and 30
            self.image = self.attack_image
            target.take_damage(attack_power)
            self.is_attacking = True
            self.last_attack_time = current_time
            self.projectile = Projectile(self.rect.center, self.direction, self.stop_distance)
        elif current_time - self.last_attack_time >= self.attack_time:
            self.image = self.move_image

    def update(self, screen, targets):
        if isinstance(targets, Character):
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
                
        elif isinstance(targets, Castle):
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
        if self.projectile:
            self.projectile.update()
            if self.projectile.distance_traveled >= self.stop_distance:
                self.is_attacking = False  # Reset attacking state
                self.projectile = None  # Remove projectile

        # Call superclass update method
        super().update()
            
        
    def draw(self, screen):
        super().draw(screen)
        if self.projectile:
            self.projectile.draw(screen)

class WarriorC(Character):
    def __init__(self, start_position, direction):
        super().__init__(
            move_image_path = os.path.join(Config.IMAGE_PATH, "warrior_c1.png"), 
            attack_image_path = os.path.join(Config.IMAGE_PATH, "warrior_c2.png"), 
            attack_power = random.randint(80, 120), 
            attack_time = 2, 
            attack_interval = 2, 
            is_single_target = False, 
            attack_range = 80, 
            health = 100, 
            stop_distance = Config.WARRIOR_SIZE // 2 + 120, 
            speed = 2, 
            start_position=start_position, 
            direction=direction
        )

    def attack(self, target):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            self.image = self.attack_image
            target.take_damage(self.attack_power)
            self.is_attacking = True
            self.last_attack_time = current_time
        elif current_time - self.last_attack_time >= self.attack_time:
            self.image = self.move_image
        


    def update(self, screen, targets):
        if isinstance(targets, Character):
            # 如果目标是战士且方向与自己不同，进行攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
                
        elif isinstance(targets, Castle):
            # 如果目标是城堡，直接攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
        
        self.draw(screen)

class WarriorD(Character):
    def __init__(self, start_position, direction):
        super().__init__(
            move_image_path = os.path.join(Config.IMAGE_PATH, "warrior_d1.png"), 
            attack_image_path = os.path.join(Config.IMAGE_PATH, "warrior_d2.png"), 
            attack_power = random.randint(20, 60), 
            attack_time = 2, 
            attack_interval = 1, 
            is_single_target = False, 
            attack_range = 50, 
            health = 300, 
            stop_distance = Config.WARRIOR_SIZE // 2 + 30, 
            speed = 7, 
            start_position=start_position, 
            direction=direction
        )

    def attack(self, target):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_interval:
            self.image = self.attack_image
            target.take_damage(self.attack_power)
            self.is_attacking = True
            self.last_attack_time = current_time
        elif current_time - self.last_attack_time >= self.attack_time:
            self.image = self.move_image
        


    def update(self, screen, targets):
        if isinstance(targets, Character):
            # 如果目标是战士且方向与自己不同，进行攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
                
        elif isinstance(targets, Castle):
            # 如果目标是城堡，直接攻击
            distance_to_target = abs(self.rect.centerx - targets.rect.centerx)
            if distance_to_target <= self.stop_distance:
                self.attack(targets)
            else:
                self.move()
                self.image = self.move_image
        
        self.draw(screen)

