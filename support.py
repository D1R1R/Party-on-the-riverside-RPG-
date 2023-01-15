import os, sys
import sqlite3
import pygame


class Support():
    def __init__(self):
        # for animation
        self._animations = {"run": [], "runback": [], "idle": [],
                 "atk": [],"take_hit": [], "death": [], "defend": [],}
        self._frame_index = 0
        self._animatoin_speed = 0.2
        self._past = "idle"
        # for plot
        self._data = None

    def load_image(self, path: str, folder: str, name: str) -> None:
        fullname = os.path.join(path, folder, name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname).convert_alpha()
        return image

    def choose_frame(self, status) -> pygame.Surface and str:
        # loop over frame index
        if self._past != status:
            self._frame_index = 0
        frames = self._animations[status]
        if self._frame_index != -1:
            self._frame_index += self._animatoin_speed
        if len(frames) <= self._frame_index:
            self._frame_index = 0
            if status == "defend" or status == "atk" or status == "sp_atk" or status == "take_hit":
                status = "idle"
            if status == "death":
                self._frame_index = -1
        self._past = status
        return (frames[int(self._frame_index)], status)

    def import_animation(self, path: str, animation_name: str) -> list:
        # animation_name == name of file with images
        full_path =  os.path.join(path, animation_name)
        surface_list = []
        for *sth, image_files in os.walk(full_path):
            for imgs in sorted(image_files, key=lambda x: int(x[x.index("_") + 1:-4])):
                img_surface = pygame.image.load(full_path + "/" + imgs).convert_alpha()
                surface_list.append(img_surface)
        if len(surface_list) == 0:
            print(f"Папка с изображениями '{animation_name}' не найден. путь: '{full_path}'")
            sys.exit()
        self._animations[animation_name] = surface_list 

    def check_bd(self, screen, answ):
        db = sqlite3.connect("data.db")
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS "userpass" (
            "username"  TEXT,
            "password"  TEXT,
            "act"  INTEGER,
            "point"  INTEGER)""")
        db.commit()
        name, password = answ
        sql.execute(f"SELECT username, password FROM userpass WHERE username = '{name}' AND password = '{password}'")
        db.commit() 
        if sql.fetchone():
            return True
        return False

    def update_bd(self, screen, answ):
        db = sqlite3.connect("data.db")
        sql = db.cursor()
        name, password = answ
        sql.execute(f"INSERT INTO userpass VALUES (?,?,1,1)", (name, password))
        db.commit()
        self.reg(screen)

    def pause(self, screen) -> None:
        pause = True
        bg = pygame.image.load("icons//pause.png")
        while pause:
            window_size = pygame.display.get_window_size()
            screen.blit(bg, (window_size[0] // 3, window_size[1] // 4))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    pause = False

    def game(self, screen) -> None:
        game = True
        bg = pygame.image.load("bg.png")
        
        WHITE = (255, 255, 255)
        text = ["PARTY ON THE",
        "RIVERSIDE (RPG)...",
        "press <return> to start!"]
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
                    game = False

    def reg(self, screen, status=False) -> None:
        game = True
        bg = pygame.image.load("bg.png")
        widgets = pygame.sprite.Group()

        bt_name = InputButton(screen, "inbutton1.png", (220, 100), widgets)
        bt_password = InputButton(screen, "inbutton2.png", (220, 250), widgets)
        answers = [bt_name.get(),  bt_password.get()]
        if status:
            bt_yes = ClickButton(screen, "fbt2.png", (220, 400), answers, widgets)
        else:
            bt_yes = ClickButton(screen, "fbt1.png", (220, 400), answers, widgets)
            bt_yes2 = ClickButton(screen, "fbt3.png", (520, 600), answers, widgets)
        
        WHITE = (255, 255, 255)
        while game:
            window_size = pygame.display.get_window_size()
            # bg
            screen.blit(bg, (0, 0))
            pygame.draw.polygon(screen, WHITE, 
                    [[0, window_size[1]], [0, 0],
                    [window_size[0] // 5, 0], [window_size[0] // 2.5, window_size[1]],])
            pygame.draw.aalines(screen, WHITE, True, 
                    [[0, window_size[1]], [0, 0],
                    [window_size[0] // 5, 0], [window_size[0] // 2.5, window_size[1]],])
            # buttons
            widgets.draw(screen)
            widgets.update()

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            if not status:
                if bt_yes.get_status():
                    game = False



class InputButton(pygame.sprite.Sprite):
    def __init__(self, sc, widget_name: str, pos: tuple, *group):
        super().__init__(*group)

        self._sp = Support()
        self._screen = sc

        pos_x, pos_y = pos
        self.text = ''
        path = 'icons'
        self.image = self._sp.load_image(path, '', widget_name)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def activate(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def render_text(self):
        font = pygame.font.SysFont('ArialBold', 65)
        text_surface = font.render(self.text, False, (212, 175, 55))
        self._screen.blit(text_surface,
                    (self.rect.x + 30, self.rect.y + 50))

    def get(self):
        return self.text

    def update(self):
        self.render_text()
        self.activate()



class ClickButton(pygame.sprite.Sprite):
    def __init__(self, sc, widget_name: str, pos: tuple, text: list, *group):
        super().__init__(*group)

        self._sp = Support()
        self._screen = sc

        pos_x, pos_y = pos
        self._type = widget_name
        if self._type == 'fbt1.png':
            self._status = False
        self.answer = text
        path = 'icons'
        self.image = self._sp.load_image(path, '', widget_name)
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def get_status(self):
        if self._type == 'fbt1.png':
            return self._status

    def activate(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self._type == 'fbt1.png':
                        if not self._status:
                            self._status = self._sp.check_bd(self._screen, self.answer)
                    elif self._type == 'fbt2.png':
                        self._sp.update_bd(self._screen, self.answer)
                    else:
                        self._sp.reg(self._screen, True)

    def update(self):
        self.activate()



class Plot():
    def __init__(self):
        self._sp = Support()
        self._curent_act, self._curent_point = 1, 1
        self._max_in_act = 20

    def get_point(self, name: str):
        with open(f'plot//{self._curent_act}//{self._curent_point}//{name}.txt', 'r') as file:
            lines = file.readlines()
            lines = [x.rstrip() for x in lines]
            text, pos, ispointlast = lines
        if ispointlast == "1":
            self.next_point()
        return text, pos

    def next_point(self):
        self._curent_point += 1
        if self._max_in_act < self._curent_point:
            self._curent_point = 1
            self._curent_act += 1    



class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, size):
        width, height = size
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
