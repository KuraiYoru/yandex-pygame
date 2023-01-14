import pygame

from settings import *
from tile import Tile
from hero import Hero, Aim
from helth_bar import Bar
from enemies import Enemy, Golem


class Level:
    def __init__(self, screen):

        self.display_surface = pygame.display.get_surface()
        # sprite group setup

        self.visible_sprites = Camera()

        self.all_sprites = pygame.sprite.Group() # группа всех спрайтов
        self.bullets = pygame.sprite.Group() # группа пуль
        self.tiles = pygame.sprite.Group() # группа блоков
        self.earth = Earth()
        self.earth.rect.x = 100
        self.earth.rect.y = 100
        self.enemies = pygame.sprite.Group() # группа врагов
        self.enemies_lst = []
        self.hero_group = pygame.sprite.Group() # группа героя
        self.golem_bullets = pygame.sprite.Group()#  группа вражеских пуль
        self.create_map()
        self.screen = screen

    def run(self):
        self.visible_sprites.update()

        # Destroy bullets-tiles
        pygame.sprite.groupcollide(self.bullets, self.tiles, True, False)

        pygame.sprite.groupcollide(self.golem_bullets, self.tiles, True, False)

        if pygame.sprite.groupcollide(self.golem_bullets, self.hero_group, True, False): # урон герою
            self.hero.hp -= 5

        for i in pygame.sprite.groupcollide(self.bullets, self.enemies, True, False).items(): # урон врагам
            i[1][0].hp -= self.hero.damage

        for i in self.enemies_lst:
            i.updater(self.hero.rect.x + self.hero.rect.width // 2, self.hero.rect.y + self.hero.rect.height // 2)

        self.visible_sprites.custom_draw(self.hero)
        self.bar.update()
        self.bar.draw(WIDTH * 0.01, HEIGHT * 0.01, self.screen)


    def create_map(self):
        self.visible_sprites.add(self.earth)
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    tile = Tile((x + 100, y + 100), [self.all_sprites])
                    self.tiles.add(tile)
                    self.visible_sprites.add(tile)
                elif col == 'p': # отрисовка блоков
                    self.half_width = self.display_surface.get_size()[0] // 2
                    self.half_height = self.display_surface.get_size()[1] // 2

                    self.aim = Aim(0, 0) # создание героя
                    self.hero = Hero(6, 6, 0, self.visible_sprites, self.bullets, self.tiles, x + 100, y + 100, self.aim)
                    self.aim.x = self.hero.rect.centerx - self.half_width
                    self.aim.y = self.hero.rect.centery - self.half_height

                    # self.all_sprites.add(self.hero)
                    self.visible_sprites.add(self.aim)
                    self.visible_sprites.add(self.hero)
                    self.bar = Bar(self.hero)
                    self.hero_group.add(self.hero)
                elif col.isdigit(): # создание врага
                    self.enemy = Golem(x + 100, y + 100, 1.5, self.enemies, self.enemies_lst, self.visible_sprites, self.golem_bullets, self.tiles)


class Camera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height # отрисовка в зависимости от расположения героя (камера)

        for sprite in self.sprites():
            if type(sprite) == Aim:
                offset_position = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, (offset_position.x + player.help_x, offset_position.y + player.help_y))
            else:
                offset_position = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_position)


class Earth(pygame.sprite.Sprite): # спрайт земли
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/earth.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (len(WORLD_MAP[0]) * TILESIZE, len(WORLD_MAP) * TILESIZE))
