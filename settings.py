import ctypes
from generation_map import Map

try:
    WIDTH, HEIGHT = tuple(map(lambda x: ctypes.windll.user32.GetSystemMetrics(x), (0, 1))) # размер экрана
except:
    WIDTH, HEIGHT = list(map(lambda x: int(x), input("Введите размер экрана в формате **** ****. Example 1920 1080").split()))
FPS = 60
TILESIZE = 64  # размер блоков
x, y = 60, 60


def creation_map():
    WORLD_MAP = Map((x, y))
    WORLD_MAP = WORLD_MAP.create_mobs()
    if WORLD_MAP == 0:
        return creation_map()
    else:
        for j in range(len(WORLD_MAP[0])):
            WORLD_MAP[0][j] = 'x'
            WORLD_MAP[-1][j] = 'x'
            WORLD_MAP[j][0] = 'x'
            WORLD_MAP[j][-1] = 'x'
        return WORLD_MAP

