from .KnowledgeBase import *


class Agent(object):
    quiver = 9999
    LEFT = 0
    RIGHT = 1
    pos = (0, 0)
    direction = -1
    kb: KnowledgeBase = None
    game = None
    #breeze = died = glimmer = have_gold = stench = False
    sensor = {
        'breeze': False,
        'died': False,
        'glimmer': False,
        'have_gold': False,
        'stench': False
    }

    def __init__(self):
        self.quiver = 9999
        self.pos = (0, 0)
        self.sensor = {
            'breeze': False,
            'died': False,
            'glimmer': False,
            'have_gold': False,
            'stench': False
        }

    def start(self, game):
        self.game = game
        self.kb = KnowledgeBase(self.game.size)
        self.direction = DIRECTIONS.NORTH
        self.kb.register_move(self.pos[0], self.pos[1])
        while(True):
            self.infer()

    def infer(self):
        pass

    def move(self):
        if self.game.move_agent() == False:
            print("Cannot move")
        x, y = self.pos
        self.kb.register_move(x, y)
        self.process_percept(x, y)

    def process_percept(self, x: int, y: int):
        if self.sensor['glimmer'] == True:
            self.kb.tell_glimmer(x, y)
        if self.sensor['breeze'] == False and self.sensor['stench'] == False:
            self.kb.tell_clear(x, y)
            return
        if self.sensor['breeze']:
            self.kb.tell_breeze(x, y)
        if self.sensor['stench']:
            self.kb.tell_stench(x, y)

    def turn(self,  direction: int):
        self.game.turn_agent(direction)
        self.kb.register_turn(direction)

    def shoot(self):
        self.quiver -= 1
        print("Use an arrow!!!")
        self.game.process_shot()
        self.process_percept(pos[0], pos[1])

    def pickup(self):
        self.game.agent_grab_gold()
        print("pickd up gold")
