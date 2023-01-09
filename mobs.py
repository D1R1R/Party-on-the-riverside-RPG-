import os, sys
import pygame, pyttsx3

from support import Support, Plot


class Aggressive_Mob(pygame.sprite.Sprite):
    def __init__(self, npc_name: str, file_name: str, pos: tuple, *group: any) -> None:
        super().__init__(*group)

        self._sp = Support()
        self._width = self._height = 43
        pos_x, pos_y = pos

        path = 'npc_animations//' + npc_name  # npc_name == file_name
        self.image = self._sp.load_image(path, "idle", file_name)
        self.rect = self.image.get_rect().move(
            self._width * pos_x, self._height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        # for animation
        self._status = "idle"
        for animation_name in ["run", "runback", "idle", "sp_atk", "take_hit", "atk", "death", "defend",]:
            self._sp.import_animation(path, animation_name)
        # specifications
        self._hp = 100
        self._dmg = 10
        self._wait = 10

    def move(self, player) -> None:
        width, height = pygame.display.get_window_size()
        px, py = (player.rect.x, player.rect.y)
        if (
            ((self.rect.x + self._width * 5) <= width and self.rect.x >= 0)
            and
            ((self.rect.y + self._height * 5) <= height and self.rect.y >= 0)
            ):
            if py != self.rect.y:
                if py > self.rect.y:
                    if px > self.rect.x:
                        self._status = "run"
                        self.rect.x, self.rect.y = (self.rect.x + 1), (self.rect.y + 1)
                    elif px < self.rect.x:
                        self._status = "runback"
                        self.rect.x, self.rect.y = (self.rect.x - 1), (self.rect.y + 1)
                    else:
                        self._status = "run"
                        self.rect.y = self.rect.y + 1
                if py < self.rect.y:
                    if px > self.rect.x:
                        self._status = "run"
                        self.rect.x, self.rect.y = (self.rect.x + 1), (self.rect.y - 1)
                    elif px < self.rect.x:
                        self._status = "runback"
                        self.rect.x, self.rect.y = (self.rect.x - 1), (self.rect.y - 1)
                    else:
                        self._status = "run"
                        self.rect.y -= 1
            else:
                if pygame.sprite.collide_mask(self, player):
                    self.atk("atk", player)
                    if player._status == "atk" and player._act:
                        self._status = "take_hit"
                        self._hp -= player._dmg
                        player._act = False
                else:
                    if px > self.rect.x:
                        self._status = "run"
                        self.rect.x += 1
                    elif px < self.rect.x:
                        self._status = "runback"
                        self.rect.x -= 1
                    else:
                        self._status = "idle"
        else:
            self._status = "idle" 

    def atk(self, atk_type: str, player) -> None:
        if player._status == "take_hit" or player._status == "death":
            pass
        elif player._status == "defend":
            if self._wait == 0:
                self._wait = 100
                self._status = atk_type
            self._wait -= 1
        else:
            if self._wait == 0:
                self._wait = 100
                self._status = atk_type
                player._status = "take_hit"
                player._hp -= self._dmg
            self._wait -= 1

    def update(self, plot=False, player=False) -> None:
        if player:
            if self._hp > 0 and self._status != "take_hit":
                self.image, self._status = self._sp.choose_frame(self._status)
                self.move(player) 
            else:
                self.image, self._status = self._sp.choose_frame(self._status)
                if self._hp <= 0:
                    self._status = "death"



class Speaking_Mob(pygame.sprite.Sprite):
    def __init__(self, npc_name: str, gen: str, file_name: str, pos: tuple, *group: any) -> None:
        super().__init__(*group)

        self._sp = Support()
        self.tts = pyttsx3.init()
        self._width = self._height = 43
        pos_x, pos_y = pos

        path = 'npc_animations//' + npc_name  # npc_name == file_name
        self.image = self._sp.load_image(path, "idle", file_name)
        self.rect = self.image.get_rect().move(
            self._width * pos_x, self._height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        # for animation
        self._status = "idle"
        for animation_name in ["idle"]:
            self._sp.import_animation(path, animation_name)
        # specifications
        self._name = npc_name
        self._active = True
        self._act = 0

        self._gender = gen
        if self._gender == "male":
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"  # david
        elif self._gender == "female":
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"  # zira
        else:
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"  # irina
        self.tts.setProperty('voice', voice_id) 

        self._text = self._sp.get_my_text()

    def move(self, player, plot) -> None:
        if pygame.sprite.collide_mask(self, player):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]: 
                text = plot.get_point(self._name)[0]
                self.speach(text) 
                self._active = False
        else:
            self._active = True

    def speach(self, text: str) -> None:
        if self._active:
            self.tts.say(text)
            self.tts.runAndWait()

    def update(self, plot=False, player=False) -> None:
        if player and plot:
            self.image, self._status = self._sp.choose_frame(self._status)
            self.move(player, plot)
