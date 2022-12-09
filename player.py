import time
import pygame

from objects import Object


YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (72, 77, 76)



class Player(Object):
    def field_of_view(self, obj_positions: tuple) -> True or False:
        fov = 20  # field_of_view
        return True

    def calculate_hp(self) -> int:
        hp = 100 - self._taken_dmg
        if hp <= 0:
            self._status = "death"
        return (hp)

    def calculate_hit(self) -> int:
        atk = 23
        return atk
    
    def take_hit(self) -> None:
        for mobs in self.nps_list:
            if self.filed_of_view((mobs._x, mobs._y)):
                if mobs._atk:
                    self._taken_dmg += mobs.calculate_hit()
                    self.calculate_hp()

    def give_hit(self) -> None:
        self.calculate_hp()

    def move(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: 
            self._y -= 1
            if not self._active:
                self._status = "run"
                self._active = True
        
        if keys[pygame.K_d]:
            self._x += 1
            if not self._active:
                self._status = "run"
                self._active = True
            elif self._status == "runback":
                self._status = "run"
            
        if keys[pygame.K_s]:
            self._y += 1
            if not self._active:
                self._status = "run"
                self._active = True
            
        if keys[pygame.K_a]:
            self._x -= 1
            if not self._active:
                self._status = "runback"
                self._active = True
            elif self._status == "run":
                self._status = "runback"

        if (not keys[pygame.K_w] and not keys[pygame.K_d]
            and not keys[pygame.K_s] and not keys[pygame.K_a]):
            self._active = False
            self.draw((self._x, self._y), (41, 39, 39))
            self._status = "idle"
        else:
            self.draw((self._x, self._y), GRAY)

    def update(self):
        if self._status == "idle" or self._status == "run" or self._status == "runback":
            self.move()
        else:
            self.draw((self._x, self._y), GRAY)
            if self._frame_index == -1 and self._status == "death":
                self.game_over((100, 100))
    
    def game_over(self, position: tuple) -> None:
        print("game over!")
        resurrect = False
        while not resurrect:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    resurrect = True
                    # reset settings:
                    self._taken_dmg = 0
                    self._x, self._y = position
                    self._frame_index = 0
                    self._animatoin_speed = 0.10
                    self._status = "idle"
                elif keys[pygame.K_x]:
                    print(22)
