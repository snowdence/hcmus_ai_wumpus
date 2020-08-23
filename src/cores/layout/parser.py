import sys
import os
import setting
import gpath
from ..wumpus.environment import WumpusWorldEnv

# try:
#     import setting
#     import gpath
#     from cores.wumpus.enviroment import WumpusWorldEnv
# except:
#     sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
#     print(sys.path)
#     import setting
#     import gpath
#    # from cores.wumpus.enviroment import WumpusWorldEnv


class Parser:
    def __init__(self):
        print("Init parser")

    def try_load(self, name):
        if not os.path.exists(name):
            return None
        with open(name) as f:
            try:
                return [line.strip() for line in f]
            finally:
                f.close()

    def load_wumpus_env(self, name) -> WumpusWorldEnv:
        lines = self.try_load(name)
        if (lines is None):
            return None
        else:
            return WumpusWorldEnv(lines)


if __name__ == '__main__':
    p = Parser()
    loaded_map = p.load_wumpus_env(gpath.PATH_MAP + 'map_4_4.txt')
    print("Test parser")
