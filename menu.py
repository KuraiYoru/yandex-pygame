import select
import pygame

import pygame_menu
from settings import *



def menu(func, screen):
    font = 'fonts/font.ttf'
    # [(0, 64, -13, 51, 77), (0, 64, -13, 51, 77), (0, 0, 0, 0, 77), (0, 64, -13, 51, 77), (0, 64, -13, 51, 77),
    #  (0, 64, -13, 51, 77), (0, 64, -13, 51, 77)]
    title = 'fonts/for_title.ttf'
    mytheme = pygame_menu.Theme(
        widget_font=font,
        title_background_color=(4, 47, 126),
        title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
        widget_selection_effect=pygame_menu.widgets.HighlightSelection(),
        title_offset=((WIDTH // 2 - len('My game'), 0)),
        title_font=title,
        title_font_size=100
    )

    myimage = pygame_menu.baseimage.BaseImage(
        image_path='sprites/213.jpg',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL

    )
    mytheme.background_color = myimage
    # self.widget_selection_effect = self._get(kwargs, 'widget_selection_effect', Selection,
    #                                          HighlightSelection(margin_x=0, margin_y=0))

    menu = pygame_menu.Menu('My game', WIDTH, HEIGHT, theme=mytheme)


    menu.add.button('Play', func)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)