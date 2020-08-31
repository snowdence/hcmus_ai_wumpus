import utils
from cores.layout.parser import Parser
from cores.search.bfs import *

map = [
    ['.', '?', '?', '?'],
    ['.', '.', '.', '?'],
    ['.', '.', '?', '.'],
    ['.', '.', '.', '.']
]

map = [['.', '.', '.', '.'],
       ['.', '.', '?', '.'],
       ['.', '.', '.', '?'],
       ['.', '?', '?', '?']]

print(map[::-1][:])

maze_problem = MazeProblem(
    4, 4,
    map, MazeState(0, 0), MazeState(0, 3))
bfs = BFS()
result, closed, cost = bfs.search(maze_problem, True)
result_action_code = [
    rslt_item.actionCode for rslt_item in result]
print(result_action_code)
print("Solved")
print("TEST BFS")
