from ..utils import *


class KBEncode:
    OK = -1
    WUMPUS = 1
    PIT = 2
    WALL = 3

    NOT_SOLVED = '?'


class KB(object):
    shape = (0, 0)
    kb_map = []
    kb_wumpus_map = []  # can be wumpus
    kb_pit_map = []  # can be pit
    kb_increase_adj = []

    kb_glu_wumpus = []
    kb_glu_pit = []

    def __init__(self, row, col):
        self.shape = (row, col)
        self.kb_map = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]
        self.kb_wumpus_map = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]
        self.kb_pit_map = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]
        self.kb_increase_adj = gen_matrix_reverse(row)

    def tell(self, position, state):
        """Add sentence

        Args:
            sentence ([type]): [description]
        """
        c, r = position  # x, y
        self.kb_map[r][c] = state

    def get_kb_wumpus(self):
        kb_gen = []

        pass

    def ask(self, query):
        pass

    def perceive_cell(self, x, y):
        """CEll perceive will be mark as CLEAR or OK

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """

        pass


if __name__ == "__main__":
    pass
