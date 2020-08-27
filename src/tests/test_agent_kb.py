import utils
import unittest
# pylint: disable=import-error
from cores.kb_solve.game import Game
from cores.kb_solve.kb_agent import *
from cores.layout.parser import Parser
import gpath
import numpy as np
if __name__ == '__main__':
    print("tets agent")
    agent = KBAgent()
    p = Parser()
    loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_4_4.txt')
    map_encode = np.rot90(loaded_map.map_encode, k=1, axes=(1, 0))
    #map_tranform = np.rot90(map_encode, k=-1, axes=(1, 0))
    game = Game(4, agent, map_encode)
    agent.start(game)
    print("End test")
