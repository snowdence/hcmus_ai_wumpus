import copy


class RoomEncodeChar:
    PIT = 'P'
    BREEZE = 'B'
    WUMPUS = 'W'
    VISITED = 'V'
    STENCH = 'S'
    GOLD = 'G'
    OK = 'O'
    EMPTY = '-'

    NOT_SOLVED = '?'


class WumpusWorldEnv:
    score = 0
    gold = 0
    wumpus = 0
    explored = []

    line_array: [] = []
    # height, width  (row, col)
    shape = (0, 0)
    map_encode: [[]] = [[]]  # matrix hxw
    map_solved: [[]] = [[]]  # matrix

    # 13 14 15 16 #0
    # 9 10 11 12  #1
    # 5 6 7 8     #2
    # 1 2 3 4     #3

    def __init__(self, line_array: [] = None):
        print("Wumpus World Env")

        if line_array != None:
            self.parse_lines_array(line_array)

    def parse_lines_array(self, lines: []):
        self.shape = (int(lines[0]), int(lines[0]))

        self.map_encode = [
            [RoomEncodeChar.EMPTY for i in range(self.width)] for j in range(self.height)
        ]
        self.map_solved = [
            [RoomEncodeChar.NOT_SOLVED for i in range(self.width)] for j in range(self.height)
        ]

        self.score = 0

        self.line_array = lines[1:].copy()

        # parse use top left
        for (r, line_row) in enumerate(self.line_array, start=0):
            cell = line_row.split('.')
            for (c, cell) in enumerate(cell, start=0):
                self.map_encode[r][c] = cell
                # self.set_room_encode_str(r, c, cell)  # set to map_encode
                if RoomEncodeChar.GOLD in cell:
                    self.gold += 1
                elif RoomEncodeChar.WUMPUS in cell:
                    self.wumpus += 1

    def set_world_size(self, h, w):
        """h : height, row
           w : width ,col

        Args:
            h ([type]): [description]
            w ([type]): [description]
        """
        self.shape = (h, w)

    def get_world_size(self):
        return self.shape

    @property
    def height(self):
        return self.shape[0]

    @property
    def width(self):
        return self.shape[1]

    def set_room_encode_str(self, x: int, y: int, value):
        """Set str of room x, y with rules bottom left

        Args:
            x (int): [description]
            y (int): [description]
            value (string): Value of cell SBG
        """
        self.map_encode[self.height - y - 1][x] = value

    def get_room_encode_str(self, x: int, y: int) -> str:
        """Return str of room x, y with rules bottom left
        Args:
            x (int): [description]
            y (int): [description]
        Returns:
            str: Current room string SGB
        """
        # sample (0,0) => map_encode[4-0-1]  = map_encode[3]

        return self.map_encode[self.height - y - 1][x]

    def get_room_solved_str(self, x: int, y: int) -> str:
        """Get solved state

        Args:
            x (int): [description]
            y (int): [description]

        Returns:
            str: [description]
        """
        return self.map_solved[self.height - y - 1][x]

    def set_room_solved_str(self, x: int, y: int, value):
        """Set solved state to matrix map

        Args:
            x (int): [description]
            y (int): [description]
            value ([type]): [description]
        """
        self.map_solved[self.height - y - 1][x] = value

    def is_solved(self, x, y):
        return self.map_solved[self.height - y - 1][x] != RoomEncodeChar.NOT_SOLVED

    def has_breeze(self, x, y):
        return RoomEncodeChar.BREEZE in self.get_room_solved_str(x, y)

    def has_pit(self, x, y):
        return RoomEncodeChar.PIT in self.get_room_solved_str(x, y)

    def has_wumpus(self, x, y):
        return RoomEncodeChar.WUMPUS in self.get_room_solved_str(x, y)

    def has_stench(self, x, y):
        return RoomEncodeChar.STENCH in self.get_room_solved_str(x, y)

    def has_gold(self, x, y):
        return RoomEncodeChar.GOLD in self.get_room_solved_str(x, y)

    def has_empty(self, x, y):
        return RoomEncodeChar.EMPTY in self.get_room_solved_str(x, y)
