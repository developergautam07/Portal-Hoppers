import pygame as pg
from settings import *
from sprites import *
import pytmx

class Map:
    def __init__(self, fn):
        self.data = []
        with open(fn, "rt") as m:
            for line in m:
                self.data.append(line.strip())

        self.tile_wid = len(self.data[0])
        self.tile_hei = len(self.data)
        self.width = self.tile_wid * TILESIZE
        self.height = self.tile_hei * TILESIZE

class Tiled_map:
    def __init__(self, filename):
        tile_m = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tile_m.width * tile_m.tilewidth
        self.height = tile_m.height * tile_m.tileheight
        self.tmxdata = tile_m

    def render(self, surface):
        tile_id = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = tile_id(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def load_map(self):
        surface = pg.Surface((self.width, self.height))
        self.render(surface)
        return surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect( 0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        # Limiting map movement towards Left
        x = min(0, x)  # min -ve value reached by map along x axis

        # Limiting map towards Top
        y = min(0, y)  # min -ve value reached by map along y axis

        # Limiting map towards Right
        x = max(-(self.width - WIDTH), x)  # max -ve value reached by map along x axis

        # Limiting map towards Bottom
        y = max(-(self.height - HEIGHT), y) # max -ve value reached by map along y axis
        self.camera = pg.Rect(x, y, self.width, self.height)