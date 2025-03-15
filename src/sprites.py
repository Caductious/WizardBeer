import random
import pygame
from settings import HEIGHT, WIDTH, gnome, player, beer

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
    def __init__(self, x, y):
        self.image = beer
        self.x, self.y = x, y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speedy = 10

    def beer_cast(self):
        self.y -= self.speedy

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))