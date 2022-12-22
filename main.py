import random

import pygame
import sys
from pygame import mixer
from settings import *
from level import Level
# from camera import *
from enemies import Enemy



BLACK = (0, 0, 0)
# TEST
class Game:
    def __init__(self):


        pygame.init()

        pygame.mixer.init()
        mixer.init()
        mixer.music.load('music/stranger-things-124008.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill((50, 50, 50))
        pygame.display.set_caption('Spritesheets')

        bg_img = pygame.image.load('sprites/bg.png').convert_alpha()
        self.bg = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

        pygame.mouse.set_visible(True)
        self.fire = []

        self.level = Level(self.screen)
        self.level.visible_sprites.add()
        self.shoot_time = pygame.time.get_ticks()

        # self.camera = Camera(self.level.hero)
        # follow = Follow(self.camera, self.level.hero)
        # self.camera.setmethod(follow)


    def run(self):
        i = 0
        shooting = False

        while True:
            self.clock.tick(FPS)
            self.screen.fill((50, 50, 50))

            # TEST

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()
                # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                #     enemy = Enemy(self.level.hero.rect.x, self.level.hero.rect.y, self.level.enemies, self.level.enemies_lst)
                #     self.level.visible_sprites.add(enemy)
                #     self.level.enemies.add(enemy)
                #     self.level.enemies_lst.append(enemy)

            if self.level.hero.hp <= 0:
                sys.exit()

            self.screen.blit(self.bg, (0, i))
            self.screen.blit(self.bg, (0, HEIGHT + i))
            if i == -HEIGHT:
                self.screen.blit(self.bg, (0, HEIGHT+i))
                i = 0
            i -= 1
            self.level.run()


            # self.camera.scroll()
            # pygame.sprite.groupcollide(mobs, bullets, True, True)

            # self.all_sprites.draw(self.screen)

            pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()