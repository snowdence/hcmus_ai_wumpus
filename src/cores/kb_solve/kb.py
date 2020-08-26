from ..utils import *


class KBEncode:
    OK = -1
    WUMPUS = 1
    PIT = 2
    WALL = 3

    NOT_SOLVED = '?'


class DIRECTIONS:
    UP = (0, 1)  # North UP South DOWN West LEFT EAST RIGHT
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    l_directions = [UP, DOWN, RIGHT, LEFT]


class KB(object):

    shape = (0, 0)
    kb_map = []
    kb_wumpus_map = []  # can be wumpus
    kb_pit_map = []  # can be pit
    kb_increase_adj = []  # 100 99 98 ....

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

    def perceive(self, x, y):
        """CEll perceive will be mark as CLEAR or OK
        - if perceive a cell add to kb clause
        - resolve if necessary
        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.kb_map[r][c] = KBEncode.OK

    def ask(self, position):
        pass

    def get_all_adj(self, x, y, i_kernel=[-1, 0, 1], j_kernel=[-1, 0, 1]):
        res = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ii = i + y
                jj = j + x
                if self.validCell(ii, jj,  self.shape) and self.kb_increase_adj[ii][jj] not in res:
                    res.append(self.kb_increase_adj[ii][jj])
        return res

    def get_all_adj_4_direction(self, x, y):
        res = []
        for dir in DIRECTIONS.l_directions:
            ii = y + dir[1]  # y
            jj = x + dir[0]
            if self.validCell(ii, jj,  self.shape):
                item = self.kb_increase_adj[ii][jj]
                if item not in res:
                    res.append(item)
        return res

    def validCell(self, i, j, shape):
        return 0 <= i and i < shape[0] and 0 <= j and j < shape[1]
