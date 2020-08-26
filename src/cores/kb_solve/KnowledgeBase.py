import os


class DIRECTIONS:
    UP = (0, 1)  # North UP South DOWN West LEFT EAST RIGHT
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    NORTH = (0, 1)
    SOUTH = (0, -1)
    EAST = (1, 0)
    WEST = (-1, 0)
    l_directions = [UP, DOWN, RIGHT, LEFT]
    LM_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]


class KnowledgeBase:
    CLEAR = -1
    move_stack = []
    turn_stack = []
    wumpus_map = []
    pit_map = []
    path_map = []
    glimmer = []

    steps = 0
    shape = (4, 4)

    def __init__(self,  size: int):
        self.wumpus_map = [[0 for i in range(size)] for j in range(size)]
        self.pit_map = [[0 for i in range(size)] for j in range(size)]
        self.path_map = [[0 for i in range(size)] for j in range(size)]
        self.glimmer = []
        self.move_stack = []
        self.turn_stack = []
        self.steps = 0
        self.shape = (size, size)

    def perceive(self, x, y, map):
        for d in DIRECTIONS.LM_DIRECTIONS:
            if (x + d[0] >= 0 and x + d[0] < len(map) and y + d[1] >= 0 and y + d[1] < len(map)):
                map[x + d[0]][y + d[1]] = self.CLEAR

    def register_move(self, x: int, y: int):
        move = (x, y)
        self.move_stack.append(move)
        self.wumpus_map[x][y] = self.CLEAR
        self.pit_map[x][y] = self.CLEAR
        self.path_map[x][y] += 1
        print("Register move")

    def register_turn(self, dir: int):
        if dir == 0 or dir == 1:
            self.turn_stack.append(dir)
        else:
            print("Invalid direction")

    def tell_clear(self, x, y):
        for d in DIRECTIONS.LM_DIRECTIONS:
            if (x + d[0] >= 0 and x + d[0] < len(self.path_map) and y + d[1] >= 0 and y + d[1] < len(self.path_map)):
                self.wumpus_map[x + d[0]][y + d[1]] = self.CLEAR
                self.pit_map[x + d[0]][y + d[1]] = self.CLEAR

    def ask_path(self, x, y):
        if self.validCell(x, y) == False:
            return 100
        return self.path_map[x][y]

    def tell_stench(self, x, y):
        if self.path_map[x][y] <= 1:
            self.perceive(x, y, self.wumpus_map)

    def ask_wumpus(self, x, y):
        if self.validCell(x, y) == False:
            return 100
        return self.wumpus_map[x][y]

    def tell_breeze(self, x, y):
        if self.path_map[x][y] <= 1:
            self.perceive(x, y, self.pit_map)

    def ask_pit(self, x, y):
        if self.validCell(x, y) == False:
            return 100
        return self.pit_map[x][y]

    def tell_glimmer(self, x, y):
        self.glimmer.append([x, y])

    def ask_glimmer(self, x, y):
        if self.validCell(x, y) == False:
            return 100
        for item in self.glimmer:
            if item[0] == x and item[1] == y:
                return True
        return False

    def validCell(self, i, j):
        return 0 <= i and i < self.shape[0] and 0 <= j and j < self.shape[1]

    def print(self):
        x = 0
        y = len(self.path_map) - 1
        while y >= 0:
            if x == 0:
                print(str(y) + "|", end="")
            for x in range(len(self.path_map)):
                last_x = self.move_stack[len(self.move_stack) - 1][0]
                last_y = self.move_stack[len(self.move_stack) - 1][1]

                if last_x == x and last_y == y:
                    print("o ", end="")
                elif self.path_map[x][y] > 0:
                    print("+ ", end="")
                elif self.wumpus_map[x][y] < 0 and self.pit_map[x][y] < 0:
                    print("  ", end="")
                elif self.wumpus_map[x][y] == 0 and self.pit_map[x][y] == 0:
                    print("? ", end="")
                elif self.wumpus_map[x][y] >= self.pit_map[x][y]:
                    print("W ", end="")
                elif self.pit_map[x][y] > 0:
                    print("P ", end="")
                else:
                    print("! ", end="")
            x = 0
            print("")
            y -= 1
        print(" ")
        for i in range(len(self.path_map)):
            print("--", end="")
        print("\n ")
        for i in range(len(self.path_map)):
            print(" " + str(i), end="")
        print("")


if __name__ == "__main__":
    kb = KnowledgeBase(4)

    kb.register_move(0, 0)
    kb.tell_clear(0, 0)

    kb.print()

    kb.register_move(1, 0)
    kb.tell_breeze(1, 0)

    kb.register_move(0, 0)
    kb.register_move(0, 1)
    kb.tell_stench(0, 1)

    kb.register_move(1, 1)
    kb.tell_clear(1, 1)

    kb.register_move(1, 2)
    kb.tell_breeze(1, 2)

    kb.tell_stench(1, 2)

    #kb.register_move(2, 1)
    #kb.tell_breeze(2, 1)

    kb.print()
    print("KN =")
