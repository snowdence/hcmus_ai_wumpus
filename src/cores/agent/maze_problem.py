from .problem import Problem
from .maze_state import MazeState
from .action import Action


class MazeProblem(Problem):
    start = 0
    goal = 0

    def __init__(self, width, height, graph, start: MazeState, goal: MazeState):
        self.start = start
        self.goal = goal
        self.graph = graph
        self.width = width
        self.height = height

    def initialState(self):
        return self.start

    def goalState(self):
        return self.goal

    def actions(self, s: MazeState):
        ms = s
        list_actions = []
        if ms.x > 0 and self.graph[ms.x - 1][ms.y] not in ['W', 'P', '?']:
            list_actions.append(Action(0))
        if ms.y > 0 and self.graph[ms.x][ms.y-1] not in ['W', 'P', '?']:
            list_actions.append(Action(1))
        if ms.x < self.width - 1 and self.graph[ms.x+1][ms.y] not in ['W', 'P', '?']:
            list_actions.append(Action(2))
        if ms.y < self.height - 1 and self.graph[ms.x][ms.y+1] not in ['W', 'P', '?']:
            list_actions.append(Action(3))
        return list_actions

    # list_state
    def result(self, s: MazeState, a: Action):
        # list_action = []
        # list_action.append(MazeState(a.actionCode, self.graph[a.actionCode]))
        ms = s
        result_state = []
        if a.actionCode == 0:
            result_state.append(MazeState(ms.x - 1, ms.y))
        elif a.actionCode == 1:
            result_state.append(MazeState(ms.x, ms.y - 1))
        elif a.actionCode == 2:
            result_state.append(MazeState(ms.x + 1, ms.y))
        elif a.actionCode == 3:
            result_state.append(MazeState(ms.x, ms.y + 1))
        return result_state

    def goalTest(self, s: MazeState):
        return s.x == self.goal.x and s.y == self.goal.y
