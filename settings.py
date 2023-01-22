import ctypes
from random import choice
import sqlite3

try:
    WIDTH, HEIGHT = tuple(map(lambda x: ctypes.windll.user32.GetSystemMetrics(x), (0, 1))) # размер экрана
except:
    WIDTH, HEIGHT = list(map(lambda x: int(x), input("Введите размер экрана в формате **** ****. Example 1920 1080").split()))
FPS = 60
TILESIZE = 64  # размер блоков
x, y = 60, 60


# def creation_map():
#     WORLD_MAP = Map((x, y))
#     WORLD_MAP = WORLD_MAP.create_mobs()
#     if WORLD_MAP == 0:
#         return creation_map()
#     else:
#         for j in range(len(WORLD_MAP[0])):
#             WORLD_MAP[0][j] = 'x'
#             WORLD_MAP[-1][j] = 'x'
#             WORLD_MAP[j][0] = 'x'
#             WORLD_MAP[j][-1] = 'x'
#         return WORLD_MAP


con = sqlite3.connect('maps.db')
cur = con.cursor()

def game_map():
    con = sqlite3.connect('maps.db')
    cur = con.cursor()
    cur.execute("SELECT file_map FROM maps")
    data = cur.fetchall()
    data = choice(data)[0]
    file_output = open("map1.txt", "wb")
    file_output.write(data)
    file_output.close()
    con.close()
    return list(map(lambda x: x.strip(),  open("map1.txt").readlines()))





