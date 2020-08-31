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


class Player(GameObject):
    def __init__(self, tile_manager, position, visible=True, tile_size=None):
        super().__init__(position=position, tile_size=tile_size,
                         image_file=gpath.PATH_IMAGE + "3x/player_1.png")
        self.tile_manager = tile_manager
        self.visible = visible

    def tile_render(self, surface):
        self.render(surface)
