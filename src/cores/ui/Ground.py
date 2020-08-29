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


class Ground(GameObject):
    visited = False

    def __init__(self, tile_manager, position, visible=True,  tile_size=None):
        super().__init__(position=position, tile_size=tile_size,
                         image_file=gpath.PATH_IMAGE + "debug_ground.png")
        self.tile_manager = tile_manager
        self.visible = visible
        self.visited = False

    def mark_visited(self):
        if self.visited == False:
            self.visited = True
            self.change_img(image_file=gpath.PATH_IMAGE + "ground1.png")
        else:
            self.change_img(image_file=gpath.PATH_IMAGE + "debug_ground.png")

    def tile_render(self, surface):
        self.render(surface)
