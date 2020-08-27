import utils
import unittest
# pylint: disable=import-error
from cores.kb_solve.kb import KB
from cores.kb_solve.glu_agent import *
from cores.layout.parser import Parser

import gpath


class GluAgentTest(unittest.TestCase):
    def test(self):
        pass


if __name__ == "__main__":
    print("Gluagent")
    p = Parser()
    loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_10_10.txt')
    glu_agent = GluAgent(loaded_map)
    while glu_agent.finished != True and glu_agent.has_solved_safe_node():
        glu_agent.get_action()

    print("opned all safe node and gold is " + str(len(glu_agent.gold_list)))
    # glu_agent.get_action()
    print("Edn test")
