import sys
import pygame
from support import Support
from mobs import Aggressive_Mob, Speaking_Mob



class MapSupport():
    def __init__(self, wall, top, *group) -> None:
        sp = Support()

        self._top = top
        self._wall = wall
        self._tile_group = group
        self._map_images = {
            'bb': sp.load_image('tiles', 'down', 'block.png'),
            'wall': sp.load_image('tiles', 'down', 'wall.png'),
            'wall_': sp.load_image('tiles', 'down', 'wall_2.png'),
            'grass': sp.load_image('tiles', 'down', 'grass_1.png'),
            'flow': sp.load_image('tiles', 'down', 'flowers.png'),
            'empty': sp.load_image('tiles', 'down', 'grass_2.png'),
            'sea': sp.load_image('tiles', 'down', 'sea.png'),
            'sea/': sp.load_image('tiles', 'down', 'sea_1.png'),
            'sea|': sp.load_image('tiles', 'down', 'sea_4.png'),
            'sea_': sp.load_image('tiles', 'down', 'sea_2.png'),
            'tree1': sp.load_image('tiles', 'medium', 'tree_1.png'),
            'tree2': sp.load_image('tiles', 'medium', 'tree_2.png'),
        }

    def load_level(self, path) -> None:
        try:
            with open(path, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]
            return level_map 
        except:
            print(f"Файл с картой поврежден!")
            sys.exit()

    def generate_level(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                # DO NOT USE "+"
                if level[y][x] == '.':
                    Tile(self._map_images, 'empty', x, y, self._tile_group)
                elif level[y][x] == '%':
                    Tile(self._map_images, 'bb', x, y, self._tile_group)
                elif level[y][x] == '!':
                    Tile(self._map_images, 'grass', x, y, self._tile_group)
                elif level[y][x] == '&':
                    Tile(self._map_images, 'sea', x, y, self._tile_group)
                elif level[y][x] == '@':
                    Tile(self._map_images, 'flow', x, y, self._tile_group)
                elif level[y][x] == '#':
                    Tile(self._map_images, 'wall', x, y, self._top, self._wall)
                elif level[y][x] == '=':
                    Tile(self._map_images, 'wall_', x, y, self._top, self._wall)
                elif level[y][x] == '/':
                    Tile(self._map_images, 'sea/', x, y, self._tile_group)
                elif level[y][x] == '|':
                    Tile(self._map_images, 'sea|', x, y, self._tile_group)
                elif level[y][x] == '_':
                    Tile(self._map_images, 'sea_', x, y, self._tile_group)
                elif level[y][x] == '1':
                    Tile(self._map_images, 'tree1', x, y, self._top)
                elif level[y][x] == '2':
                    Tile(self._map_images, 'tree2', x, y, self._top)
    def generate_npc(self, level):
        for y in range(len(level)):
            for x in range(len(level[y])):
                # DO NOT USE "+"
                if level[y][x] == '$':
                    Aggressive_Mob("monk", "idle_1.png", (x, y), self._top)
                elif level[y][x] == '@':
                    Speaking_Mob('barmaid', "female", "idle_1.png", (x, y), self._top)
                elif level[y][x] == '#':
                    Aggressive_Mob("wind", "idle_1.png", (x, y), self._top)
                elif level[y][x] == '*':
                    Speaking_Mob('king', "male", "idle_1.png", (x, y), self._top)



class Tile(pygame.sprite.Sprite):
    def __init__(self, map_images: dict, tile_type: str, pos_x: int, pos_y: int, *group):
        super().__init__(*group)
        
        width = height = 64
        self.image = map_images[tile_type]
        self.rect = self.image.get_rect().move(
            width * pos_x, height * pos_y)
