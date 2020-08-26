from .agent import Agent
from .directions import DIRECTIONS


class Game(object):
    world: [[]] = None
    score = 0
    agent: Agent = None
    size = 4
    game_over = False

    def __init__(self, size, agent, map):
        self.agent = agent
        self.agent.pos = (0, 0)
        self.size = size
        self.score = 1000
        self.world = map
        print(" init game")

    def get_score(self):
        return self.score

    def move_agent(self):

        agent = self.agent
        world = self.world

        old_pos = (agent.pos[0], agent.pos[1])
        n_pos = (agent.pos[0] + agent.direction[0],
                 agent.pos[1] + agent.direction[1])
        # or world[n_pos[0]][n_pos[1]] == 'W'
        if world[n_pos[0]][n_pos[1]] == 'P':
            self.score -= 1000
            self.agent.died = True
            self.game_over = True
            print("End game now")

        self.agent.pos = n_pos

        if 'B' in world[n_pos[0]][n_pos[1]]:
            self.agent.sensor['breeze'] = True
        else:
            self.agent.sensor['breeze'] = False

        if 'S' in world[n_pos[0]][n_pos[1]]:
            self.agent.sensor['stench'] = True
        else:
            self.agent.sensor['stench'] = False

        if 'G' in world[n_pos[0]][n_pos[1]]:
            self.agent.sensor['glimmer'] = True
        else:
            self.agent.sensor['glimmer'] = False

        self.score -= 10
        return True

    def turn_agent(self, direction: int):
        if direction == self.agent.LEFT:
            print("Agent [TURN LEFT]")
            if (self.agent.direction == DIRECTIONS.NORTH):
                self.agent.direction = DIRECTIONS.WEST
            elif (self.agent.direction == DIRECTIONS.EAST):
                self.agent.direction = DIRECTIONS.NORTH
            elif (self.agent.direction == DIRECTIONS.SOUTH):
                self.agent.direction = DIRECTIONS.EAST
            elif (self.agent.direction == DIRECTIONS.WEST):
                self.agent.direction = DIRECTIONS.SOUTH
            else:
                print("Error, cannot [tURN LEFT]")
                return
        elif direction == self.agent.RIGHT:
            print("Agent [TURN RIGHT]")
            if (self.agent.direction == DIRECTIONS.NORTH):
                self.agent.direction = DIRECTIONS.EAST
            elif (self.agent.direction == DIRECTIONS.EAST):
                self.agent.direction = DIRECTIONS.SOUTH
            elif (self.agent.direction == DIRECTIONS.SOUTH):
                self.agent.direction = DIRECTIONS.WEST
            elif (self.agent.direction == DIRECTIONS.WEST):
                self.agent.direction = DIRECTIONS.NORTH
            else:
                print("Error, cannot [tURN RIGHT]")
                return
        else:
            print("Error,cannot reach0")
            return
        # score not change

    def process_shot(self):
        if(self.world[self.agent.pos[0]][self.agent.pos[1]] == 'W'):
            self.world[self.agent.pos[0]][self.agent.pos[1]] = '-'
        else:
            print("No wumpus")

    def agent_grab_gold(self):
        if self.world[self.agent.pos[0]][self.agent.pos[1]] == 'G':
            print("Collected at  {0} {1} ".format(
                self.agent.pos[0], self.agent.pos[1]))
            self.world[self.agent.pos[0]][self.agent.pos[1]] = '-'
            self.game_over = True
            self.score += 1000
            print("End game")

        else:
            print("No gold here")
