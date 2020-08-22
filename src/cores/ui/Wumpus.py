import sys
import os
import pygame
try:
    import setting
    import gpath
    from cores.ui.GameObject import GameObject
except:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
    import setting
    import gpath
    from cores.ui.GameObject import GameObject


class Wumpus(GameObject):
    def __init__(self, tile_manager, position, tile_size=None):
        super().__init__(position=position, tile_size=tile_size,
                         image_file=gpath.PATH_IMAGE + "wumpus.png")
        self.tile_manager = tile_manager

    def tile_render(self, surface):
        self.render(surface)
