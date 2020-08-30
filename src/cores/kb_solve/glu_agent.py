from .kb import *
from ..wumpus.environment import WumpusWorldEnv


def manhattan_distance(x, y):
    return sum(abs(a-b) for a, b in zip(x, y))


class GluAgent(object):
    env: WumpusWorldEnv = None
    current_pos = (0, 0)
    finished = False

    gold_list = []
    aim_gold = 0

    score = 0
    init_pos = (0, 0)

    def __init__(self, world_env, init_player_pos=(0, 0)):
        self.kb = KB(world_env.shape[0], world_env.shape[1])
        self.env = world_env
        self.finished = False
        self.aim_gold = 999
        self.score = 0
        self.init_pos = init_player_pos
        self.move(self.init_pos[0], self.init_pos[1])

    def perceive(self, x, y):
        #  Kiểm tra ô x,y có gì
        env = self.env
        if env.has_breeze(x, y) and env.has_stench(x, y):
            self.kb.tell_stench_and_breeze(x, y)
        elif env.has_breeze(x, y):
            self.kb.tell_breeze(x, y)
        elif env.has_stench(x, y):
            self.kb.tell_stench(x, y)
        elif env.has_empty(x, y):
            self.kb.tell_clear(x, y)

        if env.has_gold(x, y):
            if ((x, y) not in self.gold_list):
                self.gold_list.append((x, y))
                self.score += 100
            if len(self.gold_list) == self.aim_gold:
                self.finished = True
            else:
                print("Num golds collected = {0}".format(len(self.gold_list)))
                print(
                    "Gold at (x,y) = ({0}, {1}) +100 points".format(x, y))
        print("Perceiving")

    def move(self, x, y):
        # dịch vị trí agent tới (x,y) => Thông báo tới KB

        self.current_pos = (x, y)
        self.kb.register_move(x, y)
        self.perceive(x, y)
        self.kb.resolve()
        self.kb.print_kb()
        print("GOTO (x,y) = ({0}, {1})".format(x, y))

    def has_solved_safe_node(self):
        return len(self.kb.get_unexpanded_safe_list()) > 0

    def get_action(self):
        # Lấy bước đi tiếp theo, Lấy trong danh sách safelist
        unexpaned_safe_list = self.kb.get_unexpanded_safe_list()
        unexpaned_safe_list.sort(
            key=lambda x: manhattan_distance(x, self.current_pos))
        if len(unexpaned_safe_list) > 0:
            choose_safe = unexpaned_safe_list.pop(0)
            return choose_safe
        else:
            self.finished = True
            return self.init_pos
