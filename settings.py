import ctypes
from generation_map import Map


WIDTH, HEIGHT = tuple(map(lambda x: ctypes.windll.user32.GetSystemMetrics(x), (0, 1))) # размер экрана
FPS = 60
TILESIZE = 64 # размиер блоков
WORLD_MAP = Map((60, 60)).map
for j in range(len(WORLD_MAP[0])):
    WORLD_MAP[0][j] = 'x'
    WORLD_MAP[-1][j] = 'x'
    WORLD_MAP[j][0] = 'x'
    WORLD_MAP[j][-1] = 'x'



