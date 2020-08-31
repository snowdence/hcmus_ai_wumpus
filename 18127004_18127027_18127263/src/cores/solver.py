import os
import sys
from .wumpus.environment import WumpusWorldEnv, RoomEncodeChar


class WumpusSolver:
    env_wumpus = None
    # (0,0) => 1
    shape = (0, 0)
    glocose_map_encode = []

    def __init__(self, env: WumpusWorldEnv):
        print("--- Init solver ----")
        self.env_wumpus = env
        self.shape = env.shape

    def percept(self, x, y):
        percept = []
