from screens import EventScreen
from states import MasterState
from gpath import *
import pygame


class GameScreen(EventScreen):
    state: MasterState = None
    title_font: pygame.font.Font = None
    item_font:  pygame.font.Font = None

    def __init__(self, state):
        EventScreen.__init__(self)
        self.state = state
        print("init state", self.state.isRunning())
        print("Init game screen")
        self.title_font = pygame.font.Font(
            PATH_ASSETS + "font/BD_Cartoon_Shout.ttf", 72)
        self.item_font = pygame.font.Font(
            PATH_ASSETS + "font/BD_Cartoon_Shout.ttf", 48)

    def loop(self, window):
        self.process_input()
        self.update()
        self.render(window)

        self.clean()

    def on_exit(self):
        self.state.running = False

    def process_input(self):
        for event in pygame.event.get():
            self.on_event(event)

    def update(self):
        pass

    def render(self, window):
        pass

    def clean(self):
        pass
