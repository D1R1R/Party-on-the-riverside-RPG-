import os, sys
import pygame


class Support():
    def __init__(self):
        # for animation
        self._animations = {"run": [], "runback": [], "idle": [],
                 "atk": [], "sp_atk": [],"take_hit": [], "death": [], "defend": [],}
        self._frame_index = 0
        self._animatoin_speed = 0.1
        self._past = "idle"

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
        self._frame_index += self._animatoin_speed
        if len(frames) <= self._frame_index:
            self._frame_index = 0
            if status == "defend" or status == "atk" or status == "sp_atk":
                status = "idle"
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

    def pause(self, screen) -> None:
        pause = True
        while pause:
            window_size = pygame.display.get_window_size()
             # text
            font = pygame.font.SysFont('ArialBold', 85)
            text_surface = font.render("soon", False, (212, 175, 55))
            screen.blit(text_surface,
                        ((window_size[0] // 2) - 100, (window_size[1] // 2) - 189))
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


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    def apply(self, obj, visible_group, all_g):
        width, height = pygame.display.get_window_size()
        tile_size = 50
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if (obj.rect.x < (0 - tile_size) or obj.rect.y < (0 - tile_size)
        or obj.rect.x > width or obj.rect.y > height):
            obj.kill()
            all_g.add(obj)
        else:
            visible_group.add(obj)

    def update(self, target, size):
        width, height = size
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)