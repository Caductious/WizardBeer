import pygame
import random

from settings import (WIDTH_SCREEN, WIDTH, HEIGHT, FPS, bg, player,
                      gnome, beer, font, hs, high_score, laugh_path, music_path)

pygame.init()
pygame.mixer.init()
music = pygame.mixer.Sound(music_path)
laugh = pygame.mixer.Sound(laugh_path)
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT))
pygame.display.set_caption("Wizardbeer")
clock = pygame.time.Clock()
music.play(-1)
game_over = False


class Gnome:
    def __init__(self):
        self.image = gnome
        self.width = 128
        self.height = 128
        self.walk = 0
        self.y = 0
        self.x = random.randrange(WIDTH - self.width)
        self.speedx = random.randrange(-8, 8)
        self.speedy = random.randrange(3, 8)

    def draw(self, screen):
        screen.blit(self.image[self.walk], (self.x, self.y))


class Player:
    def __init__(self):
        self.image = player[0]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.y = HEIGHT - self.height
        self.x = WIDTH // 2.5
        self.speedx = 10

    def movement(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x -= self.speedx
        if keystate[pygame.K_RIGHT]:
            self.x += self.speedx
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Projectile:
    def __init__(self):
        self.image = beer
        self.x, self.y = player_game.x, player_game.y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speedy = 10

    def beer_cast(self):
        self.y -= self.speedy

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


def render():
    # Рендеринг
    screen.blit(bg, (0, 0))
    screen.blit(high_score, (860, 210))
    screen.blit(hp, (890, 370))
    scr = font.render(str(score), True, 'Yellow')
    screen.blit(scr, (890, 70))
    for p in projectiles:
        if p.y <= 0:
            projectiles.pop(projectiles.index(p))
        else:
            p.draw(screen)
    for g in gnomes:
        g.draw(screen)
    player_game.draw(screen)
    pygame.display.update()


# Цикл игры
gnomes = []
projectiles = []
count = 0
player_game = Player()
lives = 3
score = 0
hp = font.render(str(lives), True, 'Yellow')
hard = 3
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    count += hard
    if not game_over:
        if score > int(hs):
            with open('../high_score.txt', 'w') as file:
                file.write(str(score))
        if score >= 20 and count % 50 == 0:
            hard = 5
        for p in projectiles:
            p.beer_cast()
        new_high_score = 20
        if count % 50 == 0:
            gnomes.append(Gnome())
            laugh.play()
        player_game.movement()
        for g in gnomes:
            for p in projectiles:
                if (g.x <= p.x <= g.x + g.width) or (g.x <= p.x + p.width <= g.x + g.width):
                    if (g.y <= p.y <= g.y + g.height) or (g.y <= p.y + p.height <= g.y + g.height):
                        gnomes.pop(gnomes.index(g))
                        projectiles.pop(projectiles.index(p))
                        score += 1
            if (g.x <= player_game.x <= g.x + g.width) or (g.x <= player_game.x + player_game.width <= g.x + g.width):
                if (g.y <= player_game.y <= g.y + g.height) or (
                        g.y <= player_game.y + player_game.height <= g.y + g.height):
                    lives -= 1
                    hp = font.render(str(lives), True, 'Yellow')
                    gnomes.pop(gnomes.index(g))
            g.x += g.speedx
            g.y += g.speedy
            if (count // 10) % 4 == 0:
                g.walk = 1
            else:
                g.walk = 0
            if g.x > WIDTH - 100 or g.x < -128 or g.y > HEIGHT:
                gnomes.pop(gnomes.index(g))

    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile())
                player_game.image = player[1]
            else:
                player_game.image = player[0]
        if lives <= 0:
            game_over = True
            gnomes = []
            running = False
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    render()
pygame.quit()
