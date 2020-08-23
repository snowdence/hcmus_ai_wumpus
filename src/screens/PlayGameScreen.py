import os
import pygame
from gpath import *
from screens import GameScreen
from states import *


from cores.tile_manager import *
from cores.layout.parser import Parser


class PlayGameScreen(GameScreen):
    loaded_map = None
    tile_manager = None

    def __init__(self, state):
        GameScreen.__init__(self, state=state)
        print("Created Game Screen")

        p = Parser()
        self.loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_4_4.txt')
        self.tile_manager = TileManager(self.loaded_map)
        print("ok")

    def SnakeLoL(self, n):
        # Sq LoL filled with a range
        Sq = [[1 + i + n * j for i in range(n)] for j in range(n)]
        for row in Sq[1::2]:
            row.reverse()     # reverse odd row's columns
        return Sq[::-1][:]    # reverse order of rows

    def update(self):
        pass

    def render(self, window):
        window.fill((0, 0, 0))

        text_point = self.title_font.render(
            "HelloWorld", True, (100, 0, 0))
        window.blit(text_point, (0, 0))
        self.tile_manager.render_all_ui(window)

    def clear(self):
        pass
