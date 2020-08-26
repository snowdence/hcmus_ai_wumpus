import utils
import unittest
# pylint: disable=import-error
from cores.kb_solve.game import Game
from cores.kb_solve.kb_agent import *
from cores.layout.parser import Parser
import gpath
if __name__ == '__main__':
    print("tets agent")
    agent = KBAgent()
    p = Parser()
    loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_4_4.txt')

    game = Game(4, agent, loaded_map.map_reverse)
    agent.start(game)
    print("End test")
