import os
import sys
import setting
import gpath
from .wumpus.environment import *
from .ui import *
import pygame

from cores.kb_solve.kb import KB
from cores.kb_solve.glu_agent import *

from cores.search.bfs import *


class TileManager(object):
    env_wumpus: WumpusWorldEnv = None
    shape = (0, 0)  # height x width

    ground_group = []  # use list since cannot move
    breeze_group = []
    gold_group = []
    stench_group = []
    wumpus_group = []
    player = None
    pit_group = []
    glu_agent = None

    performing_player = True
    performing_step = []

    def __init__(self, env: WumpusWorldEnv):
        print("TileManger()")
        self.env_wumpus = env
        self.shape = env.shape
        self.tranform_buffer_ui()
        self.player = Player(self, (0, 0))
        print("Gluagent")
        self.glu_agent = GluAgent(self.env_wumpus)
        self.ui_move_player(0, 0)

    def step(self):
        while glu_agent.finished != True and glu_agent.has_solved_safe_node():
            move_pos = glu_agent.get_action()
            glu_agent.move(move_pos[0], move_pos[1])
        print("opend all safe node and gold is " +
              str(len(glu_agent.gold_list)))

    def ui_move_player(self, x, y):
        self.player.set_position(x, self.shape[1] - y - 1)
        self.glu_agent.score -= 10
        self.show_all_cell_tile(x, y)

    def show_all_cell_tile(self, x, y):
        for ground in self.ground_group:
            if ground.get_position() == (x, self.shape[1] - y - 1):
                ground.mark_visited()

        for stench in self.stench_group:
            if stench.get_position() == (x, self.shape[1] - y - 1):
                stench.show()

        for breeze in self.breeze_group:
            if breeze.get_position() == (x, self.shape[1] - y - 1):
                breeze.show()

        for gold in self.gold_group:
            if gold.get_position() == (x, self.shape[1] - y - 1):
                gold.show()

        for pit in self.pit_group:
            if pit.get_position() == (x, self.shape[1] - y - 1):
                pit.show()

    def tranform_buffer_ui(self):
        rows, cols = self.shape
        m = self.env_wumpus.map_encode
        for r in range(rows):
            for c in range(cols):
                cell = m[r][c]
                self.ground_group.append(Ground(self, (c, r)))
                if RoomEncodeChar.BREEZE in cell:
                    self.breeze_group.append(
                        Breeze(self, (c, r), visible=False)
                    )  # use top left x, y
                if RoomEncodeChar.WUMPUS in cell:
                    self.wumpus_group.append(
                        Wumpus(self, (c, r), visible=False)
                    )
                if RoomEncodeChar.GOLD in cell:
                    self.gold_group.append(
                        Gold(self, (c, r), visible=False)
                    )
                if RoomEncodeChar.PIT in cell:
                    self.pit_group.append(
                        Pit(self, (c, r), visible=False)
                    )
                if RoomEncodeChar.STENCH in cell:
                    self.stench_group.append(
                        Stench(self, (c, r), visible=False)
                    )

    def update_step(self):
        # if self.glu_agent.finished != True and self.glu_agent.has_solved_safe_node():
        #     move_pos = self.glu_agent.get_action()
        #     self.glu_agent.move(move_pos[0], move_pos[1])
        #     self.ui_move_player(move_pos[0], move_pos[1])
        # else:
        #     print("opend all safe node and gold is " +
        #           str(len(self.glu_agent.gold_list)))

        # return
        ps = len(self.performing_step)
        if ps > 0:
            (px, py) = self.player.get_position()
            (px, py) = (px, self.env_wumpus.shape[1] - py - 1)
            act = self.performing_step.pop(0)
            vect_d = (0, 0)
            if act == 0:
                vect_d = (-1, 0)
            elif act == 1:
                vect_d = (0, -1)
            elif act == 2:
                vect_d = (1, 0)
            elif act == 3:
                vect_d = (0, 1)
            new_pos = (px + vect_d[0], py+vect_d[1])
            self.ui_move_player(new_pos[0], new_pos[1])
            print("Temp move")
        else:
            if self.glu_agent.finished != True and self.glu_agent.has_solved_safe_node():
                move_pos = self.glu_agent.get_action()
                if manhattan_distance(move_pos, self.glu_agent.current_pos) > 1:
                    (px, py) = self.player.get_position()
                    map_solve = self.glu_agent.kb.get_map_solved()
                    (px, py) = (px, self.env_wumpus.shape[1] - py - 1)
                    maze_problem = MazeProblem(
                        self.env_wumpus.shape[0], self.env_wumpus.shape[1],
                        map_solve, MazeState(px, py), MazeState(move_pos[0], move_pos[1]))
                    bfs = BFS()
                    result, closed, cost = bfs.search(maze_problem, True)
                    result_action_code = [
                        rslt_item.actionCode for rslt_item in result]
                    if len(result_action_code) == 1:
                        print("crsah")
                    self.performing_step = result_action_code
                    self.glu_agent.move(move_pos[0], move_pos[1])

                else:
                    self.glu_agent.move(move_pos[0], move_pos[1])
                    self.ui_move_player(move_pos[0], move_pos[1])
            else:

                print("opend all safe node and gold is " +
                      str(len(self.glu_agent.gold_list)))

    def render_all_ui(self, surface):
        all_safe_nodes = self.glu_agent.kb.get_map_solved()
        for ground in self.ground_group:

            ground.tile_render(surface)

        for stench in self.stench_group:
            pos = stench.get_position()
            if(all_safe_nodes[pos[0]][self.shape[0] - pos[1] - 1] != "?"):
                stench.show()
            stench.tile_render(surface)

        for breeze in self.breeze_group:
            pos = breeze.get_position()
            if(all_safe_nodes[pos[0]][self.shape[0] - pos[1] - 1] != "?"):
                breeze.show()
            breeze.tile_render(surface)

        for gold in self.gold_group:
            pos = gold.get_position()
            if(all_safe_nodes[pos[0]][self.shape[0] - pos[1] - 1] != "?"):
                gold.show()
            gold.tile_render(surface)

        for pit in self.pit_group:
            pos = pit.get_position()
            if(all_safe_nodes[pos[0]][self.shape[0] - pos[1] - 1] != "?"):
                pit.show()
            pit.tile_render(surface)

        for wumpus in self.wumpus_group:
            pos = wumpus.get_position()
            if(all_safe_nodes[pos[0]][self.shape[0] - pos[1] - 1] != "?"):
                wumpus.show()
            wumpus.tile_render(surface)

        self.player.tile_render(surface)


if __name__ == "__main__":

    print("__tilemanager()__")

    print("__ end module tilemanager()__")
