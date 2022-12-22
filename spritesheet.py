import pygame


class Spritesheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, frame1, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), (frame1 * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image


def get_animation(list_of_sheet, width, height, destroy_bg, num_of_sprite, scale, starty):
    animation_list = []
    step_counterx = 0
    step_countery = starty
    for _ in range(1, num_of_sprite + 1):  # количество спрайтов в листе
        animation_list.append(list_of_sheet.get_image(step_counterx, step_countery, width, height, scale, destroy_bg))
        step_counterx += 1
    return animation_list