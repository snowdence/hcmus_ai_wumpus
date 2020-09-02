import os
import pygame
from gpath import *
from screens import GameScreen
from states import *


from cores.tile_manager import *
from cores.layout.parser import Parser


from cores.kb_solve.kb import KB
from cores.kb_solve.glu_agent import *


class PlayGameScreen(GameScreen):
    loaded_map = None
    tile_manager = None

    def __init__(self, state):
        GameScreen.__init__(self, state=state)
        print("Created Game Screen")

        p = Parser()
        self.loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_10_10.txt')
        self.tile_manager = TileManager(self.loaded_map)
        print("ok")

    def update(self):
        self.tile_manager.update_step()

    def render(self, window):
        window.fill((0, 0, 0))

        self.tile_manager.render_all_ui(window)

        text_point = self.title_font.render(
            "Score: " + str(self.tile_manager.glu_agent.score), True, (100, 0, 0))
        gold = self.title_font.render(
            "Gold: " + str(len(self.tile_manager.glu_agent.gold_list)), True, (100, 0, 0))
        step = self.title_font.render(
            "Step: " + str(len(self.tile_manager.log_ui_pos)), True, (200, 0, 0))
        safe_nodes = self.title_font.render(
            "Safe: " + str(len(self.tile_manager.glu_agent.kb.safe_nodes)), True, (200, 0, 0))

        window.blit(text_point, (640, 0))
        window.blit(gold, (640, 100))
        window.blit(step, (640, 200))
        window.blit(safe_nodes, (640, 300))

        pygame.time.wait(100)

    def clear(self):
        pass
