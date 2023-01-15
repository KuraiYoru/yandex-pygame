import pygame
from game import Game
from generation_map import Map

def run():
    WORLD_MAP = Map((60, 60)).map
    for j in range(len(WORLD_MAP[0])):
        WORLD_MAP[0][j] = 'x'
        WORLD_MAP[-1][j] = 'x'
        WORLD_MAP[j][0] = 'x'
        WORLD_MAP[j][-1] = 'x'
    game = Game()
