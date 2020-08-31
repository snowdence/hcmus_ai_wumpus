# from ..utils import *
from pysat.solvers import Solver


def gen_matrix_reverse(n=4, no_next_join=True):
    """Tạo matrix số thứ tự tăng dần theo chiều xuôi hoặc ngược

    Args:
        n (int, optional): [description]. Defaults to 4.
        no_next_join (bool, optional): [description]. Defaults to True.

    Returns:
        [type]: [description]
    """
    Sq = [[1 + i + n * j for i in range(n)] for j in range(n)]
    if no_next_join == False:
        for row in Sq[1::2]:
            row.reverse()     # reverse od d row's columns
    return Sq[::-1][:]    # reverse order of rows


def intersect(current, other):
    """Giao của 2 tập hợp

    Args:
        current ([type]): [description]
        other ([type]): [description]

    Returns:
        [type]: [description]
    """
    return type(current)([e for e in current if e in other])


def difference(current, other):
    """Có trong current nhưng không có trong other

    Args:
        current ([type]): [description]
        other ([type]): [description]

    Returns:
        [type]: [description]
    """
    return type(current)([e for e in current if e not in other])


def symmetric_difference(current, other):
    """có trong A nhưng không có trong B + có trong B nhưng không có trong A

    Args:
        current ([type]): [description]
        other ([type]): [description]

    Returns:
        [type]: [description]
    """
    return type(current)([e for e in current if e not in other] +
                         [e for e in other if e not in current])


def gen_matrix_increase(n=4, no_next_join=True):
    # Tạo ma trận tăng dần
    Sq = [[1 + i + n * j for i in range(n)] for j in range(n)]
    return Sq    # reverse order of rows


class KBEncode:
    NOT_PIT = -2
    NOT_WUMPUS = -1
    WUMPUS = 1
    PIT = 2

    NOT_SOLVED = 0


class DIRECTIONS:
    UP = (0, 1)  # North UP South DOWN West LEFT EAST RIGHT
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    l_directions = [UP, DOWN, RIGHT, LEFT]


class KB(object):

    shape = (0, 0)

    kb_map = []

    kb_increase_adj = []  # 100 99 98 ....

    kb_glu_wumpus = []
    kb_glu_pit = []
    move_stack = []

    visited_stack = []

    safe_nodes = []

    kb_solved_wumpus = []
    kb_unsolved_wumpus = []

    kb_solved_pit = []
    kb_unsolved_pit = []

    kb_map_pit = []
    kb_map_wumpus = []

    def __init__(self, row, col):
        self.shape = (row, col)
        self.kb_map = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]
        self.kb_map_pit = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]

        self.kb_map_wumpus = [
            [KBEncode.NOT_SOLVED for i in range(col)] for j in range(row)
        ]

        self.kb_increase_adj = gen_matrix_increase(self.shape[0])

        self.kb_glu_wumpus = []
        self.kb_glu_pit = []

        self.kb_solved_wumpus = []
        self.kb_unsolved_wumpus = []
        self.kb_solved_pit = []
        self.kb_unsolved_pit = []

        self.move_stack = []
        self.safe_nodes = []
        self.visited_stack = []

    def xy_to_adj(self, x, y):
        """Chuyển đổi (x,y) thành adj tăng dần (0,0) => 1

        Args:
            x ([type]): [description]
            y ([type]): [description]

        Returns:
            [type]: [description]
        """
        i, j = y, x
        return i * self.shape[1] + j + 1

    def adj_to_xy(self, adj: int):
        """return (x,y) point

        Args:
            adj (int): [description]

        Returns:
            [type]: [description]
        """
        i = int(adj / self.shape[1])
        if adj % self.shape[1] == 0:
            i -= 1
            j = self.shape[1]-1
        else:
            j = adj % self.shape[1] - 1
        return (j, i)

    def get_kb_solved_pit(self):
        """Lấy toạ độ xy các ô đã solve

        Returns:
            [type]: [description]
        """
        return [self.adj_to_xy(item) for item in self.kb_solved_pit]

    def get_kb_solved_wumpus(self):
        """Lấy toạ độ xy các ô wumpus đã solve

        Returns:
            [type]: [description]
        """
        return [self.adj_to_xy(item) for item in self.kb_solved_wumpus]

    def get_all_adj(self, x, y, i_kernel=[-1, 0, 1], j_kernel=[-1, 0, 1]):
        # Lấy các ô thuộc tính lân cận ( 9 ô)
        res = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ii = i + y
                jj = j + x
                if self.validCell(ii, jj,  self.shape) and self.kb_increase_adj[ii][jj] not in res:
                    res.append(self.kb_increase_adj[ii][jj])
        return res

    def get_all_adj_4_direction(self, x, y):
        """Lấy ô thuộc tính có thể đi ( 4 ô UP DOWN RIGHT LEFT)

        Args:
            x ([type]): [description]
            y ([type]): [description]

        Returns:
            [type]: [description]
        """
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
        """Kiểm tra xem cell có hợp lệ không

        Args:
            i ([type]): [description]
            j ([type]): [description]
            shape ([type]): [description]

        Returns:
            [type]: [description]
        """
        return 0 <= i and i < shape[0] and 0 <= j and j < shape[1]

    def register_move(self, x, y):
        """Đăng ký cho Player di chuyển đến ô (x,y)

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        move = (x, y)
        self.move_stack.append(move)
        if (x, y) not in self.visited_stack:
            self.visited_stack.append((x, y))

    def add_safe_node(self, x, y):
        """Đánh dấu x,y là safe node

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        if (x, y) not in self.safe_nodes:
            self.safe_nodes.append((x, y))

    def tell_clear(self, x, y):
        """Clear => No wumpus, No PIt around this cell

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.add_safe_node(x, y)
        l_adj = self.get_all_adj_4_direction(x, y)

        for adj in l_adj:
            (x, y) = self.adj_to_xy(adj)
            self.kb_glu_pit.append([-adj])
            self.kb_glu_wumpus.append([-adj])
            self.add_safe_node(x, y)

    def tell_breeze(self, x, y):
        """Đánh dấu ô (x,y) là breeze
        => Xung quanh không ô nào là wumpus
        => Các ô lân cận có thể là PIT 

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.add_safe_node(x, y)

        l_adj = self.get_all_adj_4_direction(x, y)
        for adj in l_adj:
            # item = self.adj_to_xy(adj)
            self.kb_glu_wumpus.append([-adj])
        self.kb_glu_pit.append(l_adj)

    def tell_stench(self, x, y):
        """Đánh dấu ô (x,y) là nhận thấy STENCH
        => Xung quanh không ô nào là PIT
        => Các ô lân cận là Wumpus
        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.add_safe_node(x, y)
        l_adj = self.get_all_adj_4_direction(x, y)
        for adj in l_adj:
            # item = self.adj_to_xy(adj)
            self.kb_glu_pit.append([-adj])
        self.kb_glu_wumpus.append(l_adj)

    def tell_stench_and_breeze(self, x, y):
        """Đánh dấu ô (x,y ) nhận thấy cả STENCH và BREEZE 
        => Các ô lân cận có thể là PIT
        => Các ô lân cận có thể là wumpus

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.add_safe_node(x, y)
        l_adj = self.get_all_adj_4_direction(x, y)

        self.kb_glu_pit.append(l_adj)
        self.kb_glu_wumpus.append(l_adj)

    def resolve_wumpus(self):
        """Giải bằng Solver, Nếu giải False tức là mệnh đề còn lại là TRue, đánh dấu ô đó ở trạng thái còn lại
        """
        self.kb_unsolved_wumpus = []
        self.kb_solved_wumpus = []

        with Solver('g3', bootstrap_with=self.kb_glu_wumpus) as s:
            for cell in range(1, self.shape[0] * self.shape[0]+1):
                x, y = self.adj_to_xy(cell)
                if s.solve(assumptions=[cell]) == False:
                    self.kb_solved_wumpus.append(cell)
                    # -cell is true => not have wumpus
                    self.kb_map_wumpus[x][y] = KBEncode.NOT_WUMPUS

                elif s.solve(assumptions=[-cell]) == False:
                    self.kb_solved_wumpus.append(cell)
                    self.kb_map_wumpus[x][y] = KBEncode.WUMPUS
                else:
                    self.kb_unsolved_wumpus.append(cell)

    def resolve_pit(self):
        """Giải bằng Solver, Nếu giải False tức là mệnh đề còn lại là TRue, đánh dấu ô đó ở trạng thái còn lại
        """
        self.kb_unsolved_pit = []
        self.kb_solved_pit = []

        with Solver('g3', bootstrap_with=self.kb_glu_pit) as s:
            for cell in range(1, self.shape[0] * self.shape[0]+1):
                x, y = self.adj_to_xy(cell)
                if s.solve(assumptions=[cell]) == False:
                    self.kb_solved_pit.append(cell)
                    # -cell is true => has wumpus
                    self.kb_map_pit[x][y] = KBEncode.NOT_PIT
                elif s.solve(assumptions=[-cell]) == False:
                    self.kb_solved_pit.append(cell)
                    self.kb_map_pit[x][y] = KBEncode.PIT
                else:
                    self.kb_unsolved_pit.append(cell)

    def resolve(self):
        """Giải PIT và wumpus, đánh dấu các ô không có PIT và wumpus là safe
        """
        self.resolve_wumpus()
        self.resolve_pit()
        for x in range(self.shape[0]):
            for y in range(self.shape[0]):
                if self.kb_map_pit[x][y] < 0 and self.kb_map_wumpus[x][y] < 0:
                    # not pit, wumpus
                    self.add_safe_node(x, y)

    def get_unexpanded_safe_list(self):
        """Danh sách ô safe chưa mở 

        Returns:
            [type]: [description]
        """
        return difference(self.safe_nodes, self.move_stack)

    def ask_wumpus(self, x, y):
        adj = self.xy_to_adj(x, y)
        if adj in self.kb_solved_wumpus:
            return -1  # solved, this cell is wumpus
        return 0

    def ask_pit(self, x, y):
        adj = self.xy_to_adj(x, y)
        if adj in self.kb_solved_pit:
            return -1  # solved, this cell is pit
        return 0

    def print_kb(self):
        """In ra Knowledgebase
        """
        print("=============  KB  ==============")
        print("Shape: {0} ".format(self.shape[0]))
        print()
        print("Visited: ")
        print(self.visited_stack)
        print()
        print("Unexpanded safe node: ")
        print(self.get_unexpanded_safe_list())
        print()
        print("Safe node: ")
        print(self.safe_nodes)
        print()
        print("Solved wumpus: ")
        print(self.kb_solved_wumpus)
        print()
        print("Solved pit: ")
        print(self.kb_solved_pit)
        print()
        print("============= <KB> ==============")
        self.print_map_solved()

    def get_map_solved(self):
        # Lấy map đã solved
        ms = [
            [KBEncode.NOT_SOLVED for i in range(self.shape[0])] for j in range(self.shape[1])
        ]
        for y in range(self.shape[0]-1, -1, -1):
            for x in range(self.shape[0]):
                if self.kb_map_wumpus[x][y] > 0 and self.kb_map_pit[x][y] < 0:  # wumpus
                    ms[x][y] = "W"
                elif self.kb_map_pit[x][y] > 0 and self.kb_map_wumpus[x][y] < 0:
                    ms[x][y] = "P"
                elif self.kb_map_pit[x][y] < 0 and self.kb_map_wumpus[x][y] < 0:
                    ms[x][y] = "OK"
                elif (x, y) in self.safe_nodes:
                    ms[x][y] = "OK"
                else:
                    ms[x][y] = "?"
        return ms

    def get_graph_bfs_solved(self):
        """Lấy map bfs để tìm đường đi ngắn nhất tới 2 điểm

        Returns:
            [type]: [description]
        """
        ms = self.get_map_solved()
        list_graph = []

        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                if ms[x][y] == "OK":
                    list_adj_xy = [
                        item for item in self.get_all_adj_4_direction(x, y)]
                    node = [item for item in list_adj_xy if ms[item[0]]
                            [item[1]] != "?"]
                    list_graph.append({self.xy_to_adj(x, y): node})
        return list_graph

    def print_map_solved(self):
        """In ra map đã solved
        """
        print("=========== Map ==================")
        for y in range(self.shape[0]-1, -1, -1):
            for x in range(self.shape[0]):
                if self.kb_map_wumpus[x][y] > 0 and self.kb_map_pit[x][y] < 0:  # wumpus
                    print("W ", end="")
                elif self.kb_map_pit[x][y] > 0 and self.kb_map_wumpus[x][y] < 0:
                    print("P ", end="")
                elif self.kb_map_pit[x][y] < 0 and self.kb_map_wumpus[x][y] < 0:
                    print("O ", end="")
                elif (x, y) in self.safe_nodes:
                    print("+ ", end="")
                else:
                    print("? ", end="")
            print()
        print("=========== Map ==================")


if __name__ == "__main__":

    print("KB")
    kb = KB(4, 4)
    kb.register_move(0, 0)
    kb.tell_clear(0, 0)  # (0,1) => OK,  (1,0) => OK

    kb.register_move(1, 0)
    kb.tell_breeze(1, 0)
    kb.resolve()

    kb.register_move(0, 1)
    kb.tell_stench(0, 1)
    kb.resolve()

    kb.register_move(1, 1)
    kb.tell_clear(1, 1)
    kb.resolve()

    kb.register_move(1, 2)
    # kb.tell_stench(1, 2)
    # kb.tell_breeze(1, 2)
    kb.tell_stench_and_breeze(1, 2)
    kb.resolve()
    kb.print_kb()

    print("End kb")
