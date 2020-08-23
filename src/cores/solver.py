import os
import sys
from .wumpus.environment import WumpusWorldEnv, RoomEncodeChar


class Solver:
    def __init__(self):
        print("--- Init solver ----")