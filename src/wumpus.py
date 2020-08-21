import pygame
from setting import *
from gpath import *
from constants import *
from states import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


class WumpusGame:
    master_state = None

    def __init__(self):
        self.window = pygame.display.set_mode(
            (GAME_SETTING.WIDTH, GAME_SETTING.HEIGHT))
        pygame.display.set_caption(GAME_SETTING.TITLE)
        pygame.display.set_icon(pygame.image.load(GAME_ICON))
        self.master_state = MasterState(
            window=self.window, running=True, screen_state=EScreenState.PLAY_GAME)
        self.clock = pygame.time.Clock()

    def run(self):
        """Main run of game
        """
        while self.master_state.isRunning():
            # blit screen on window surface
            self.master_state.getActiveScreen().loop(self.window)

            pygame.display.update()

            self.clock.tick(60)


pacman_game = WumpusGame()
pacman_game.run()
pygame.quit()
