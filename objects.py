import os
import pygame

from support import Support

YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Object():
    def __init__(self, screen, position: tuple, name: str, obj_type='obj', path=None):
        self._x, self._y = position
        self._angle = 0
        self._name = name
        self._screen = screen
        self._support = Support(file="coming soon")

        self._font = pygame.font.SysFont('Comic Sans MS', 15)
        self._current_img = ""
        # for animation:
        self._status = "idle"
        if path:
            self._frame_index = 0
            self._animatoin_speed = 0.20
            self._anim_path = path

            if obj_type == "player":
                self._animations = {"run": [], "idle": []}
            else:
                self._animations = {"status_1": [], "status_2": [], "status_3": []}
            for name in self._animations.keys():
                try:
                    self._animations[name] = self.import_animation(name)
                except:
                    print("The game files are corrupted!!!")
                    exit()
        self.draw((self._x, self._y), RED)

    def choose_frame(self) -> None:
        # loop over frame index
        frames = self._animations[self._status]
        self._frame_index += self._animatoin_speed
        if len(frames) <= (self._frame_index + 1):
            self._frame_index = 0

        self._current_img = frames[int(self._frame_index)]

    def draw(self, xy: tuple, font_color) -> None:
        self._screen.fill((0,0,0))
        # text
        text_surface = self._font.render(self._name, False, font_color)
        x, y = xy
        self._screen.blit(text_surface,
                    (x - (len(self._name) * 4), y + 10))
        # obj
        self.choose_frame()
        self._screen.blit(self._current_img, ((x, y)))

    def import_animation(self, animation_name: str) -> list:
        # animation_name == name of file with images
        full_path = self._anim_path + animation_name 
        surface_list = []
        for *sth, image_files in os.walk(full_path):
            for imgs in image_files:
                img_surface = pygame.image.load(full_path + "/" + imgs).convert_alpha()
                surface_list.append(img_surface)
        if len(surface_list) == 0:
            raise Exception('files not found')
        return surface_list