from .agent import Agent
from .directions import DIRECTIONS


class KBAgent (Agent):
    def __init__(self):
        Agent.__init__(self)

    def backtrack(self, move_stack, risk_factor: int):
        i = self.loopback(risk_factor)
        if i < 0:
            return False
        kb = self.kb
        cell = kb.move_stack[i]
        print("Backing to [{0} {1}]".format(cell[0], cell[1]))
        temp_move_stack = kb.move_stack[:]
        temp_turn_stack = kb.turn_stack[:]

        print("move stack size: {0} \t Turnstack size {1}".format(
            len(temp_move_stack), len(temp_turn_stack)))
        try:
            self.turn(self.LEFT)
            self.turn(self.LEFT)
            self.move()
            while self.pos[0] != cell[0] or self.pos[1] != cell[1]:
                next_move: list = temp_move_stack[len(temp_move_stack)-1]
                if self.pos[0] + self.direction[0] == next_move[0] and self.pos[1] + self.direction[1] == next_move[1]:
                    self.move()
                    temp_move_stack.pop()
                else:
                    turn: int = temp_turn_stack[-1]
                    if turn == self.LEFT:
                        self.turn(self.RIGHT)
                        temp_turn_stack.pop()
                    elif turn == self.RIGHT:
                        self.turn(self.LEFT)
                        temp_turn_stack.pop()
            return True
        except:
            return False

    def loopback(self, risk_factor: int):
        kb = self.kb
        i = len(kb.move_stack) - 1
        while i >= 0:
            m = self.kb.move_stack[i]
            for d in DIRECTIONS.LM_DIRECTIONS:
                x = m[0] + d[0]
                y = m[1] + d[1]
                if kb.ask_path(x, y) == 0:
                    if kb.ask_wumpus(x, y) + kb.ask_pit(x, y) <= risk_factor:
                        return i
            i -= 1
        return -1

    def infer(self):
        print("KBAgent infer")
        if self.kb.ask_glimmer(self.pos[0], self.pos[1]):
            self.pickup()
            return

        risk_factor = -2
        while(True):
            print("Infer(): pos {0},{1}\n direction {2}, {3} - risk-factor {4} ".format(
                self.pos[0], self.pos[1], self.direction[0], self.direction[1], risk_factor))
            forward_score = 99999
            left_score = 99999
            right_score = 99999
            p = self.pos
            kb = self.kb
            if self.direction == DIRECTIONS.NORTH:
                forward_score = self.kb.ask_wumpus(
                    p[0], p[1] + 1) + self.kb.ask_pit(p[0], p[1]+1) + self.kb.ask_path(p[0], p[1]+1)
                right_score = kb.ask_wumpus(
                    p[0] + 1, p[1]) + kb.ask_pit(p[0] + 1, p[1]) + kb.ask_path(p[0] + 1, p[1])
                left_score = kb.ask_wumpus(
                    p[0] - 1, p[1]) + kb.ask_pit(p[0] - 1, p[1]) + kb.ask_path(p[0] - 1, p[1])
            elif self.direction == DIRECTIONS.SOUTH:
                forward_score = kb.ask_wumpus(
                    p[0], p[1] - 1) + kb.ask_pit(p[0], p[1] - 1) + kb.ask_path(p[0], p[1]-1)
                right_score = kb.ask_wumpus(
                    p[0] - 1, p[1]) + kb.ask_pit(p[0] - 1, p[1]) + kb.ask_path(p[0] - 1, p[1])
                left_score = kb.ask_wumpus(
                    p[0] + 1, p[1]) + kb.ask_pit(p[0] + 1, p[1]) + kb.ask_path(p[0] + 1, p[1])
            elif self.direction == DIRECTIONS.EAST:
                forward_score = kb.ask_wumpus(
                    p[0] + 1, p[1]) + kb.ask_pit(p[0] + 1, p[1]) + kb.ask_path(p[0] + 1, p[1])
                right_score = kb.ask_wumpus(
                    p[0], p[1] - 1) + kb.ask_pit(p[0], p[1] - 1) + kb.ask_path(p[0], p[1] - 1)
                left_score = kb.ask_wumpus(
                    p[0], p[1] + 1) + kb.ask_pit(p[0], p[1] + 1) + kb.ask_path(p[0], p[1] + 1)
            elif self.direction == DIRECTIONS.WEST:
                forward_score = kb.ask_wumpus(
                    p[0] - 1, p[1]) + kb.ask_pit(p[0] - 1, p[1]) + kb.ask_path(p[0] - 1, p[1])
                right_score = kb.ask_wumpus(
                    p[0], p[1] + 1) + kb.ask_pit(p[0], p[1] + 1) + kb.ask_path(p[0], p[1] + 1)
                left_score = kb.ask_wumpus(
                    p[0], p[1] - 1) + kb.ask_pit(p[0], p[1] - 1) + kb.ask_path(p[0], p[1] - 1)
            else:
                print("Direction error")

            print("\tForwardDanger: {0} \n\tRightDanger:  {1} \n\t LeftDanger {2}\n\t".format(
                forward_score, right_score, left_score
            ))
            if forward_score <= risk_factor and forward_score <= left_score and forward_score <= right_score:
                self.move()
                self.kb.print()
                return
            elif left_score <= risk_factor and left_score <= right_score:
                self.turn(self.LEFT)
                self.move()
                self.kb.print()
                return
            elif right_score <= risk_factor:
                self.turn(self.RIGHT)
                self.move()
                self.kb.print()
                return
            else:
                backtracked = self.backtrack(self.kb.move_stack, risk_factor)
                if backtracked:
                    print("Backtracked ")
                    return
                else:
                    print("No suitale backtracked")

            risk_factor += 1
