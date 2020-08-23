import os
import sys
import setting
import gpath
from .wumpus.environment import *
from .ui import *
import pygame


class TileManager(object):
    env_wumpus: WumpusWorldEnv = None
    shape = (0, 0)  # height x width

    ground_group = []  # use list since cannot move
    breeze_group = []
    gold_group = []
    stench_group = []
    wumpus_group = []
    player = None
    pit_group = []

    def __init__(self, env: WumpusWorldEnv):
        print("TileManger()")
        self.env_wumpus = env
        self.shape = env.shape
        self.tranform_buffer_ui()
        self.player = Player(self, (0, 3))

    def tranform_buffer_ui(self):
        rows, cols = self.shape
        m = self.env_wumpus.map_encode
        for r in range(rows):
            for c in range(cols):
                cell = m[r][c]
                self.ground_group.append(Ground(self, (c, r)))
                if RoomEncodeChar.BREEZE in cell:
                    self.breeze_group.append(
                        Breeze(self, (c, r))
                    )  # use top left x, y
                if RoomEncodeChar.WUMPUS in cell:
                    self.wumpus_group.append(
                        Wumpus(self, (c, r))
                    )
                if RoomEncodeChar.GOLD in cell:
                    self.gold_group.append(
                        Gold(self, (c, r))
                    )
                if RoomEncodeChar.PIT in cell:
                    self.pit_group.append(
                        Pit(self, (c, r))
                    )
                if RoomEncodeChar.STENCH in cell:
                    self.stench_group.append(
                        Stench(self, (c, r))
                    )

    def render_all_ui(self, surface):

        for ground in self.ground_group:
            ground.tile_render(surface)
        for stench in self.stench_group:
            stench.tile_render(surface)

        for breeze in self.breeze_group:
            breeze.tile_render(surface)

        for gold in self.gold_group:
            gold.tile_render(surface)

        for pit in self.pit_group:
            pit.tile_render(surface)

        for wumpus in self.wumpus_group:
            wumpus.tile_render(surface)

        self.player.tile_render(surface)


if __name__ == "__main__":

    print("__tilemanager()__")

    print("__ end module tilemanager()__")
