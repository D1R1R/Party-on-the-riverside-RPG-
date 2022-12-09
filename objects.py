import os, time
import pygame


YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (72, 77, 76)


class Object():
    def __init__(self, screen, position: tuple, name: str, obj_type='obj', path=None):
        self._x, self._y = position
        self._taken_dmg = 1000
        self._name = name
        self._screen = screen
        # self._support = Support(file="coming soon")

        self._font = pygame.font.SysFont('Arial', 15)
        self._current_img = ""
        # for animation:
        self._status = "idle"
        if path:
            self._frame_index = 0
            self._animatoin_speed = 0.10
            self._anim_path = path
            self._active = False

            if obj_type == "player":
                self._animations = {"run": [], "runback": [], "idle": [],
                 "atk2": [], "jump": [], "death": [], "defend": [],}
            else:
                self._animations = {"status_1": [], "status_2": [], "status_3": []}
            for name in self._animations.keys():
                try:
                    self._animations[name] = self.import_animation(name)
                except:
                    print("The game files are corrupted!!!")
                    exit()
        self.draw((self._x, self._y), (100, 107, 106))
        
    def choose_frame(self) -> None:
        # loop over frame index
        frames = self._animations[self._status]
        self._frame_index += self._animatoin_speed
        if len(frames) <= self._frame_index:
            self._frame_index = 0
            if self._status == "atk2":
                self._status = "idle"
                self._atk = False
            elif self._status == "death":
                self._animatoin_speed = 0
                self._frame_index = -1
            
        self._current_img = frames[int(self._frame_index)]

    def draw(self, xy: tuple, font_color) -> None:
        # text
        text_surface = self._font.render(self._name, False, font_color)
        x, y = xy
        self._screen.blit(text_surface,
                    (x + (len(self._name) * 19), y + 55))
        # obj
        self.choose_frame()
        self._screen.blit(self._current_img, ((x, y)))

    def import_animation(self, animation_name: str) -> list:
        # animation_name == name of file with images
        full_path = self._anim_path + animation_name 
        surface_list = []
        for *sth, image_files in os.walk(full_path):
            for imgs in sorted(image_files, key=lambda x: int(x[x.index("_") + 1:-4])):
                img_surface = pygame.image.load(full_path + "/" + imgs).convert_alpha()
                surface_list.append(img_surface)
        if len(surface_list) == 0:
            raise Exception('files not found')
        return surface_list
