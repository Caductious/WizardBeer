import pygame


from settings import (WIDTH_SCREEN, WIDTH, HEIGHT, FPS, bg, player,
                    font, hs, laugh_path, music_path, count, lives, score)
from sprites import Player, Gnome, Projectile



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Wizardbeer")

        self.gnomes = []
        self.projectiles = []
        self.player_game = Player()

        self.music = pygame.mixer.Sound(music_path)
        self.laugh = pygame.mixer.Sound(laugh_path)
        self.screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT))
        self.count = count
        self.score = score
        self.lives = lives
        self.hs = hs
        self.hard_level = 3
        self.game_over = False
        self.running = True

        self.clock = pygame.time.Clock()
        self.high_score = font.render(hs, True, 'Yellow')
        self.hp = font.render(str(self.lives), True, 'Yellow')


    def render(self):
        # Рендеринг
        self.screen.blit(bg, (0, 0))
        self.screen.blit(self.high_score, (860, 210))
        self.screen.blit(self.hp, (890, 370))
        scr = font.render(str(self.score), True, 'Yellow')
        self.screen.blit(scr, (890, 70))
        for p in self.projectiles:
            if p.y <= 0:
                self.projectiles.pop(self.projectiles.index(p))
            else:
                p.draw(self.screen)
        for g in self.gnomes:
            g.draw(self.screen)
        self.player_game.draw(self.screen)
        pygame.display.update()

# Цикл игры
    def run(self):
        self.music.play(-1)
        while self.running:
            # Держим цикл на правильной скорости
            self.clock.tick(FPS)
            self.count += self.hard_level

            if not self.game_over:
                if self.score > int(self.hs):
                    with open('resources/high_score.txt', 'w') as file:
                        file.write(str(self.score))

                if self.score >= 20 and self.count % 50 == 0:
                    self.hard_level = 5

                for p in self.projectiles:
                    p.beer_cast()

                if self.count % 50 == 0:
                    self.gnomes.append(Gnome())
                    self.laugh.play()

                self.player_game.movement()

                for g in self.gnomes:
                    #Если гном стукнул проджектайл
                    for p in self.projectiles:
                        if (((g.x <= p.x <= g.x + g.width) or (g.x <= p.x + p.width <= g.x + g.width)) and
                        ((g.y <= p.y <= g.y + g.height) or (g.y <= p.y + p.height <= g.y + g.height))):
                            self.gnomes.pop(self.gnomes.index(g))
                            self.projectiles.pop(self.projectiles.index(p))
                            self.score += 1
                            #Если гном стукнул игрока
                    if (((g.x <= self.player_game.x <= g.x + g.width) or (g.x <= self.player_game.x + self.player_game.width <= g.x + g.width)) and
                    ((g.y <= self.player_game.y <= g.y + g.height) or (g.y <= self.player_game.y + self.player_game.height <= g.y + g.height))):
                        self.lives -= 1
                        self.hp = font.render(str(self.lives), True, 'Yellow')
                        self.gnomes.pop(self.gnomes.index(g))
                    g.x += g.speedx
                    g.y += g.speedy
                    #Анимации у гномов
                    if (self.count // 10) % 4 == 0:
                        g.walk = 1
                    else:
                        g.walk = 0
                    #Проверка на выход гнома за карту
                    if g.x > WIDTH - 100 or g.x < -128 or g.y > HEIGHT:
                        self.gnomes.pop(self.gnomes.index(g))

            #Ввод процесса (события)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.projectiles.append(Projectile(self.player_game.x, self.player_game.y))
                        self.player_game.image = player[1]
                    else:
                        self.player_game.image = player[0]
                if self.lives <= 0:
                    self.game_over = True
                    self.gnomes = []
                    self.running = False

                if event.type == pygame.QUIT:
                    self.running = False
            self.render()
        pygame.quit()
