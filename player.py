import os, sys
import pygame
import random

from support import Support


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, screen,  file_name: str, *group: any) -> None:
        super().__init__(*group)

        self._sp = Support()
        self._sc = screen

        self.image = self._sp.load_image('player_animations//leaf', "idle", file_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos)
        # for animation
        self._status = "idle"
        for animation_name in ["run", "runback", "idle", "take_hit", "atk", "death", "defend",]:
            self._sp.import_animation('player_animations//leaf', animation_name)
        # specifications
        self._act = False
        self._hp = 10
        self._dmg = 10
        # for game
        self.list_of_death = [
            "you died because you don't play well",
            "you died because mobs are better than you",
            "you died, now you have to start over"
        ]

    def player_move(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._status = "atk"
                self._act = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            self._status = "defend"
        
        if keys[pygame.K_w]: 
            self.rect.y -= 2
            self._status = "run"
        
        if keys[pygame.K_d]:
            self.rect.x += 2
            self._status = "run"
            
        if keys[pygame.K_s]:
            self.rect.y += 2
            self._status = "run"
            
        if keys[pygame.K_a]:
            self.rect.x -= 2
            self._status = "runback"
        
        if (not keys[pygame.K_w] and not keys[pygame.K_d]
            and not keys[pygame.K_s] and not keys[pygame.K_a]
            and self._status != "defend" and self._status != "atk"):
            self._status = "idle"

    def atk(self, atk_type: str) -> None:
        self._status = atk_type

    def hp_line(self, screen):
        if self._hp <= 0:
            self._status = "death"

    def game_over(self, screen):
        game = True
        bg = pygame.image.load("bg.png")
        WHITE = (255, 255, 255)
        phrase = random.choice(self.list_of_death)
        text = ["GAME OVER :'(",
        f"{phrase}...",
        "press <return> to restart!"]
        while game:
            window_size = pygame.display.get_window_size()
            level = (window_size[1] // 2) - 60
            # bg
            screen.blit(bg, (0, 0))
            pygame.draw.polygon(screen, WHITE, 
                    [[0, window_size[1]], [0, 0],
                    [window_size[0] // 5, 0], [window_size[0] // 2.5, window_size[1]],])
            pygame.draw.aalines(screen, WHITE, True, 
                    [[0, window_size[1]], [0, 0],
                    [window_size[0] // 5, 0], [window_size[0] // 2.5, window_size[1]],])
            # text
            font = pygame.font.SysFont('ArialBold', 85)
            for sentence in text[:-1]:
                text_surface = font.render(sentence, False, (212, 175, 55))
                screen.blit(text_surface,
                            ((window_size[0] // 5), level))
                level += 50
            level += 100
            font = pygame.font.SysFont('ArialBold', 35)
            text_surface = font.render(text[-1], False, (212, 175, 55))
            screen.blit(text_surface,
                        ((window_size[0] // 5), level))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self._hp = 300
                    self._status = "idle"
                    game = False

    def update(self, sc=False, boxes_group=False) -> None:
        if boxes_group:
            old_rect_x, old_rect_y = self.rect.x, self.rect.y
            self.image, self._status = self._sp.choose_frame(self._status) 
            self.hp_line(sc)
            if self._status != "death":
                if self._status != "take_hit":
                    self.player_move()
                    if pygame.sprite.spritecollideany(self, boxes_group):
                        self.rect.x, self.rect.y = old_rect_x, old_rect_y
            else:
                if self._sp._frame_index == -1:
                    self.game_over(self._sc)
