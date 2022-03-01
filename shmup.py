# Игра Shmup - 1 часть
# Cпрайты врагов
import time

import pygame
import random
import os
from os import path

WIDTH = 820
HEIGHT = 600
FPS = 60
image_folder = path.join((__file__), 'entity')

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("танки версия 0.0.1")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_image, (100, 100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        a = Ammo(self.rect.centerx, self.rect.top)
        all_sprites.add(a)
        ammon.add(a)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_mob = pygame.transform.scale(enemies, (50, 30))
        self.image_mob.set_colorkey(BLACK)
        self.image = self.image_mob.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 20)
        self.fps_spectator = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.fps_spectator > 50:
            self.fps_spectator = now
            self.rot = (self.rot + self.rot_speed) % 360
            image_new = pygame.transform.rotate(self.image_mob, self.rot)
            old_checker = self.rect.center()
            self.image = image_new
            self.rect = self.image.get_rect()
            self.rect.center = old_checker


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)





class Ammo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(blasters, (10, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# графика игры
# backgrounds = pygame.image.load(path.join(image_folder, '')).convert()
backgrounds = pygame.image.load("entity/background_number2.png").convert_alpha()
back_rect = backgrounds.get_rect()
blasters = pygame.image.load("entity/blaster.png").convert_alpha()
player_image = pygame.image.load("entity/tilled.png").convert_alpha()
enemies = pygame.image.load("entity/allien.png").convert_alpha()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
ammon = pygame.sprite.Group()

all_sprites.add(player)
for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Цикл игры
running = True
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()
    hit = pygame.sprite.groupcollide(mobs, ammon, True, True)
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(backgrounds,back_rect)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()