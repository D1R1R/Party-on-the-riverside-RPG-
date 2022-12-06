import math
import pygame

from objects import Object


YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


class Player(Object):
    def field_of_view(self, obj_positions: tuple) -> None:
        fov = 20  # field_of_view
        for obj_name, obj_coordinates in obj_positions:
            obj_x, obj_y = obj_coordinates
            if obj_x - self._x <= fov // 2:
                if obj_y - self._y < fov:
                    obj_name.status("active")
            elif obj_x - self._x < fov:
                if obj_y - self._y <= fov // 2:
                    obj_name.status("active")
            elif obj_x - self._x == fov and obj_y - self._y == 0:
                obj_name.status("active")
            elif obj_y - self._y == fov and obj_x - self._x == 0:
                obj_name.status("active")
            else:
                obj_name.status("passive")

    def move(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: 
            self._status = "run"
            self._y -= 1
            self.draw((self._x, self._y), YELLOW)
        
        if keys[pygame.K_d]:
            self._status = "run"
            self._x += 1
            self.draw((self._x, self._y), YELLOW)
            
        if keys[pygame.K_s]:
            self._status = "run"
            self._y += 1
            self.draw((self._x, self._y), YELLOW)
            
        if keys[pygame.K_a]:
            self._status = "run"
            self._x -= 1
            self.draw((self._x, self._y), YELLOW)

        if (not keys[pygame.K_w] and not keys[pygame.K_d]
            and not keys[pygame.K_s] and not keys[pygame.K_a]):
            self.draw((self._x, self._y), BLUE)
            self._status = "idle"

    def update(self):
        self.move()
        self.field_of_view(self._support.read_information())


