import sys
import os
import pygame
try:
    import setting
    import gpath
except:
    sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
    import setting
    import gpath


class GameObject(object):
    tile_size = (setting.GAME_SETTING.TILE_SIZE,
                 setting.GAME_SETTING.TILE_SIZE)
    texture: pygame.Surface = None
    position: tuple = (0, 0)

    layer_img = None
    visible = True

    def __init__(self, position: None, tile_size=None, image_file=None):
        if position != None:
            self.position = position
        else:
            self.position = (0, 0)

        if tile_size != None:
            self.tile_size = tile_size
        else:
            self.tile_size = (setting.GAME_SETTING.TILE_SIZE,
                              setting.GAME_SETTING.TILE_SIZE)

        if image_file != None:
            self.layer_img = pygame.image.load(image_file)
            self.texture = pygame.transform.scale(
                self.layer_img, (64, 64)
            )
        else:
            self.texture = pygame.Surface((64, 64))
            self.texture.fill((100, 0, 0))  # red as default

    def change_img(self, image_file):
        self.layer_img = pygame.image.load(image_file)
        self.texture = pygame.transform.scale(
            self.layer_img, (64, 64)
        )

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def fill_default(self, val):
        """Fill default color for tile

        Args:
            val ( (R,G,B) ): RGB color
        """
        self.texture.fill(val)

    def set_position(self, x, y):
        self.position = (x, y)

    def get_position(self):
        return self.position

    def render(self, surface, position=None, angle=None):
        if self.visible == False:
            return
        if position != None:
            self.set_position(position[0], position[1])

        texture_rect = pygame.Rect(
            0, 0, setting.GAME_SETTING.TILE_SIZE, setting.GAME_SETTING.TILE_SIZE)

        if angle is None:
            surface.blit(self.texture, (self.position[0] * setting.GAME_SETTING.TILE_SIZE,
                                        self.position[1] * setting.GAME_SETTING.TILE_SIZE), texture_rect)


if __name__ == "__main__":
    print("__GameObject__")
    print("__End GameObject__")
