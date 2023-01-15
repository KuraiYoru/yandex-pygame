import pygame
import sys
from pygame import mixer
from settings import *
from level import Level

from menu import Menu



BLACK = (0, 0, 0)
# TEST
class Game:
    def __init__(self):

        pygame.init()

        pygame.mixer.init()
        mixer.init()
        mixer.music.load('music/song18.mp3')
        mixer.music.set_volume(0.3)
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
        self.enemies = self.level.enemies


    def run(self): # основной цикл игры
        i = 0
        paused = False

        while True:
            if len(self.enemies) == 0:
                start("You win!")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if paused:
                        paused = False
                    else:
                        paused = True

            if self.level.hero.hp <= 0:
                start("You lose!")

            if not paused:
                self.clock.tick(FPS)
                self.screen.fill((50, 50, 50))
                self.screen.blit(self.bg, (0, i))  # движение заднего фона
                self.screen.blit(self.bg, (0, HEIGHT + i))
                if i == -HEIGHT:
                    self.screen.blit(self.bg, (0, HEIGHT + i))
                    i = 0
                i -= 1

                self.level.run()


                pygame.display.flip()
            else:
                font = pygame.font.Font(None, 128)
                text = font.render("GAME PAUSED!", True, (15, 144, 182))
                text_x = WIDTH // 2 - text.get_width() // 2
                text_y = HEIGHT // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                self.screen.blit(text, (text_x, text_y))
                pygame.draw.rect(self.screen, (0, 0, 0), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 5)
                pygame.display.flip()


def start(condition):

    game = Game()
    menu = Menu(game.run, game.screen, condition)




if __name__ == "__main__":
    start("")
