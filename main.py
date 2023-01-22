import pygame

from player import Player
from support import Support, Camera, Plot
from map import MapSupport


WINDOW_SIZE = (1300, 700)
FPS = 65
RED = (255, 0, 0)


def main(size) -> None:
    pygame.init()
    pygame.font.init()
    sp = Support()
    camera = Camera()
    clock = pygame.time.Clock()
    width, height = size

    pygame.display.set_caption("PartyOnTheRiverside")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    all_sprites = pygame.sprite.Group()

    top = pygame.sprite.Group()
    wall = pygame.sprite.Group()

    players = pygame.sprite.Group()

    player = Player((200, 155), screen, "idle_1.png", all_sprites, players)
    map = MapSupport(wall, top, all_sprites)

    map.generate_level(map.load_level("map.txt"))
    # npc
    map.generate_npc(map.load_level("map_npc.txt"))
    # top
    map.generate_level(map.load_level("map_top.txt"))
    running = True
    sp.game(screen)
    sp.reg(screen)
    plot = Plot()
    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.atk("atk")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                player.atk("sp_atk")
            if keys[pygame.K_p]:
                sp.pause(screen)
            if keys[pygame.K_l]:
                main(WINDOW_SIZE)

        screen.fill((0, 0, 0))
        # camera
        camera.update(player, size)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in top:
            camera.apply(sprite)
        # map
        all_sprites.draw(screen)
        all_sprites.update()
        # PLAYER
        players.draw(screen)
        players.update(screen, wall)
        # top
        top.draw(screen)
        top.update(plot, player)

        elem = pygame.image.load("icons//gui.png")
        screen.blit(elem, (0, 0))
        font = pygame.font.SysFont('ArialBold', 55)
        text_surface = font.render(str(player._hp), False, (212, 175, 55))
        screen.blit(text_surface, (175, 35))
        font = pygame.font.SysFont('ArialBold', 35)
        text_surface = font.render(
            'press <p> to to pause; press <l> to exit',
            False, (212, 175, 55))
        screen.blit(
            text_surface,
            (size[0] // 3, 0))

        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main(WINDOW_SIZE)
