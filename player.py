import os, sys
import pygame

from support import Support


class Player(pygame.sprite.Sprite):
    def __init__(self,  file_name: str, *group: any) -> None:
        super().__init__(*group)

        self._sp = Support()

        self.image = self._sp.load_image('player_animations//leaf', "idle", file_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # for animation
        self._status = "idle"
        for animation_name in ["run", "runback", "idle", "sp_atk", "take_hit", "atk", "death", "defend",]:
            self._sp.import_animation('player_animations//leaf', animation_name)
        # specifications
        self._hp = 100
        self._dmg = 10

    def move(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._status = "atk"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            self._status = "defend"
        
        if keys[pygame.K_w]: 
            self.rect.y -= 1
            self._status = "run"
        
        if keys[pygame.K_d]:
            self.rect.x += 1
            self._status = "run"
            
        if keys[pygame.K_s]:
            self.rect.y += 1
            self._status = "run"
            
        if keys[pygame.K_a]:
            self.rect.x -= 1
            self._status = "runback"
        
        if (not keys[pygame.K_w] and not keys[pygame.K_d]
            and not keys[pygame.K_s] and not keys[pygame.K_a]
            and self._status != "defend" and self._status != "atk"
            and self._status != "sp_atk"):
            self._status = "idle"

    def atk(self, atk_type: str) -> None:
        self._status = atk_type

    def update(self, obj=None) -> None:
        self.image, self._status = self._sp.choose_frame(self._status) 
        self.move()