import pygame
import spritesheet
import math
from settings import WIDTH, HEIGHT
from projectile import Projectile

BLACK = (0, 0, 0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, enemies, enemy_lst, all_sprites, tiles): # x y - положение , enemies - группа спрайтов врагов, enemy_llst - лист врагов питоновский, группа всех спрайтов
        pygame.sprite.Sprite.__init__(self)
        self.facing = 0
        self.animation_list = []
        self.action = 0  # 0-idle 1-walk 2-death
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.vel = vel
        self.float_x = x
        self.float_y = y
        self.hp = 100
        self.enemies = enemies
        self.enemy_lst = enemy_lst
        self.enemies.add(self)
        self.enemy_lst.append(self)
        self.live = True
        self.animation_cooldown = 100
        self.all_sprites = all_sprites
        self.all_sprites.add(self)
        self.tiles = tiles

        self.moving = True


    def updater(self, direction_x, direction_y):

        if not self.facing:
            self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False) # смена кадров анимации
            self.image.set_colorkey(BLACK)
        else:
            self.image = self.animation_list[self.action][self.frame_index]
            self.image.set_colorkey(BLACK)
        if pygame.time.get_ticks() - self.update_time >= self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 2:
                    self.kill()
                    for i in range(len(self.enemy_lst)):
                        if id(self) == id(self.enemy_lst[i]):
                            del self.enemy_lst[i]
                            break

        if self.action != 2 and self.moving:  # движение врагов
            x_diff = direction_x - self.rect.x
            y_diff = direction_y - self.rect.y

            self.angle = math.atan2(y_diff, x_diff)
            self.change_x = math.cos(self.angle) * self.vel
            self.change_y = math.sin(self.angle) * self.vel

            self.float_y += self.vel * int(self.change_y)
            self.float_x += self.vel * int(self.change_x)
            prevx = self.rect.x
            prevy = self.rect.y
            self.rect.x = int(self.float_x)
            self.rect.y = int(self.float_y)
            if pygame.sprite.spritecollide(self, self.tiles, False):
                self.rect.x = prevx
                self.rect.y = prevy
            if direction_x > self.rect.x:
                self.facing = True
            else:
                self.facing = False
            self.action = 1


        if self.hp <= 0:
            self.action = 2


class Golem(Enemy):

    def __init__(self, x, y, vel, enemies, enemy_lst, all_sprites, bullets, tiles):
        super().__init__(x, y, vel, enemies, enemy_lst, all_sprites, tiles)
        self.action = 0  # 0-idle 1-going 2-dying 3-defending 4-shoot
        self.animation_list = golem_lst
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_cooldown = 150
        self.bullets = bullets
        self.shoot_time = pygame.time.get_ticks()
        self.shooting = False


        self.flag = False
        self.strike_laser = False

    def updater(self, direction_x, direction_y):
        super().updater(direction_x, direction_y) # наследование движения и анимации


        if pygame.time.get_ticks() - self.shoot_time >= 3000 and self.action != 2: # стрельба
            self.shooting = True
            self.moving = False
            self.shoot_time = pygame.time.get_ticks()
        if self.shooting:
            self.action = 4
        if self.action == 4 and self.frame_index == 8:
            self.shoot(2, direction_x, direction_y, shoot_list1, self.bullets)
            self.shoot_time = pygame.time.get_ticks()
            self.shooting = False
            self.moving = True
            self.frame_index = 0


    def shoot(self, vel, direction_x, direction_y, sprite_list, bullets_type): # функция стрельбы
        if not self.facing:
            bullet = Projectile(vel, self.rect.x, self.rect.y + self.rect.y * 0.1, direction_x, direction_y - self.rect.y * 0.1, sprite_list)
        else:
            bullet = Projectile(vel, self.rect.x + self.rect.width, self.rect.y + self.rect.y * 0.1, direction_x, direction_y - self.rect.y * 0.1, sprite_list)
        self.all_sprites.add(bullet)
        bullets_type.add(bullet)
        return bullet


sprite_sheet_idle1 = pygame.image.load('sprites/gladiator.png').convert_alpha()
show_idle1 = spritesheet.Spritesheet(sprite_sheet_idle1)
idle_1_list = spritesheet.get_animation(show_idle1, 32, 32, BLACK, 7, 4, 2)

# Sprites for golem
sprite_sheet_idle = pygame.image.load('sprites/Golem1.png').convert_alpha() # пример создания типа анимации бег, стрельба и тд
show_idle = spritesheet.Spritesheet(sprite_sheet_idle)
idle_list = spritesheet.get_animation(show_idle, 54, 50, BLACK, 4, 6, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem2.png').convert_alpha()
defence = spritesheet.Spritesheet(sprite_sheet_idle)
defence_list = spritesheet.get_animation(defence, 53, 48, BLACK, 8, 6, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem3.png').convert_alpha()
die = spritesheet.Spritesheet(sprite_sheet_idle)
die_list = spritesheet.get_animation(die, 60, 78, BLACK, 14, 6, 0)

sprite_sheet_idle = pygame.image.load('sprites/Golem4.png').convert_alpha()
shoot = spritesheet.Spritesheet(sprite_sheet_idle)
shoot_list = spritesheet.get_animation(shoot, 77, 49, BLACK, 9, 6, 0)

sprite_sheet_idle = pygame.image.load('sprites/GolemArm.png').convert_alpha()
shoot = spritesheet.Spritesheet(sprite_sheet_idle)
shoot_list1 = spritesheet.get_animation(shoot, 35, 14, BLACK, 6, 6, 0)

sprite_sheet_idle = pygame.image.load('sprites/Shoot1.png').convert_alpha()
laser = spritesheet.Spritesheet(sprite_sheet_idle)
laser_start = spritesheet.get_animation(laser, 36, 39, BLACK, 8, 3, 0)

sprite_sheet_idle = pygame.image.load('sprites/Shoot2.png').convert_alpha()
laser_go = spritesheet.Spritesheet(sprite_sheet_idle)
laser_strike = spritesheet.get_animation(laser_go, 272, 48, (255, 255, 255), 6, 4, 0)

golem_lst = []  # добавление всей анимации
golem_lst.append(idle_list)
golem_lst.append(idle_list)
golem_lst.append(die_list)
golem_lst.append(defence_list)
golem_lst.append(shoot_list)
