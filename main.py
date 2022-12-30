import pygame
from player2 import Player
from mobs import Mob
from support import Support, Camera
from map import MapSupport


WINDOW_SIZE = (1000, 600)
FPS = 1000
RED = (255, 0, 0)

def main(size) -> None:
    pygame.init()
    pygame.font.init()
    sp = Support()
    camera = Camera()
    clock = pygame.time.Clock()
    width, height = size

    pygame.display.set_caption("Прямоугольник")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    
    all_sprites = pygame.sprite.Group()

    visible_group = pygame.sprite.Group()
    top = pygame.sprite.Group()

    players = pygame.sprite.Group()
    creatures = pygame.sprite.Group()

    player = Player("idle_1.png", visible_group, all_sprites, players)

    map = MapSupport(top, visible_group, all_sprites)
    # monk = Mob("monk", "idle_1.png", all_sprites, creatures)
    map.generate_level(map.load_level("map.txt"))
    # top
    map.generate_level(map.load_level("map_top.txt"))
    running = True
    sp.game(screen)
    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.atk("atk")
                # monk.atk("atk")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                player.atk("sp_atk")
                # monk.atk("sp_atk")
            if keys[pygame.K_p]:
                sp.pause(screen)

        screen.fill((0,0,0))
        # camera
        camera.update(player, size) 
        for sprite in all_sprites:
            camera.apply(sprite, visible_group, all_sprites)
        for sprite in top:
            camera.apply(sprite, top, top)
        # map
        visible_group.draw(screen)
        visible_group.update()
        # creatures
        creatures.draw(screen)
        creatures.update()
        # PLAYER
        players.draw(screen)
        players.update()
        # top
        top.draw(screen)
        top.update()
        
        clock.tick(FPS)
        pygame.display.flip()
          
                
if __name__ == '__main__':
    main(WINDOW_SIZE)
