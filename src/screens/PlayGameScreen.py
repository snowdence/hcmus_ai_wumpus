import os
import pygame
from gpath import *
from screens import GameScreen
from states import *


class PlayGameScreen(GameScreen):
    def __init__(self, state):
        GameScreen.__init__(self, state=state)
        print("Created Game Screen")

    def update(self):
        pass

    def render(self, window):
        window.fill((0, 0, 0))

        text_point = self.title_font.render(
            "HelloWorld", True, (100, 0, 0))
        window.blit(text_point, (0, 0))

    def clear(self):
        pass
