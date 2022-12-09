import pygame
from player import Player
from map import House


WINDOW_SIZE = (1000, 600)
FPS = 90
RED = (255, 0, 0)

def pause(screen) -> None:
    pause = True
    while pause:
        # draw menu
        pygame.draw.polygon(screen, (121, 85, 72), 
                    [[(WINDOW_SIZE[0] // 2) + 160, (WINDOW_SIZE[1] // 2) - 200],
                     [(WINDOW_SIZE[0] // 2) + 160, (WINDOW_SIZE[1] // 2) - 180],
                     [(WINDOW_SIZE[0] // 2) + 180, (WINDOW_SIZE[1] // 2) - 180],
                     [(WINDOW_SIZE[0] // 2) + 180, (WINDOW_SIZE[1] // 2) + 180],
                     [(WINDOW_SIZE[0] // 2) + 160, (WINDOW_SIZE[1] // 2) + 180],
                     [(WINDOW_SIZE[0] // 2) + 160, (WINDOW_SIZE[1] // 2) + 200],
                     [(WINDOW_SIZE[0] // 2) - 160, (WINDOW_SIZE[1] // 2) + 200],
                     [(WINDOW_SIZE[0] // 2) - 160, (WINDOW_SIZE[1] // 2) + 180],
                     [(WINDOW_SIZE[0] // 2) - 180, (WINDOW_SIZE[1] // 2) + 180],
                     [(WINDOW_SIZE[0] // 2) - 180, (WINDOW_SIZE[1] // 2) - 180],
                     [(WINDOW_SIZE[0] // 2) - 160, (WINDOW_SIZE[1] // 2) - 180],
                     [(WINDOW_SIZE[0] // 2) - 160, (WINDOW_SIZE[1] // 2) - 200],])
        pygame.draw.polygon(screen, (161, 136, 127), 
                    [[(WINDOW_SIZE[0] // 2) + 149, (WINDOW_SIZE[1] // 2) - 189],
                     [(WINDOW_SIZE[0] // 2) + 149, (WINDOW_SIZE[1] // 2) - 169],
                     [(WINDOW_SIZE[0] // 2) + 169, (WINDOW_SIZE[1] // 2) - 169],
                     [(WINDOW_SIZE[0] // 2) + 169, (WINDOW_SIZE[1] // 2) + 169],
                     [(WINDOW_SIZE[0] // 2) + 149, (WINDOW_SIZE[1] // 2) + 169],
                     [(WINDOW_SIZE[0] // 2) + 149, (WINDOW_SIZE[1] // 2) + 189],
                     [(WINDOW_SIZE[0] // 2) - 149, (WINDOW_SIZE[1] // 2) + 189],
                     [(WINDOW_SIZE[0] // 2) - 149, (WINDOW_SIZE[1] // 2) + 169],
                     [(WINDOW_SIZE[0] // 2) - 169, (WINDOW_SIZE[1] // 2) + 169],
                     [(WINDOW_SIZE[0] // 2) - 169, (WINDOW_SIZE[1] // 2) - 169],
                     [(WINDOW_SIZE[0] // 2) - 149, (WINDOW_SIZE[1] // 2) - 169],
                     [(WINDOW_SIZE[0] // 2) - 149, (WINDOW_SIZE[1] // 2) - 189],])
        # text
        font = pygame.font.SysFont('ArialBold', 85)
        text_surface = font.render("MENU:", False, (212, 175, 55))
        screen.blit(text_surface,
                    ((WINDOW_SIZE[0] // 2) - 100, (WINDOW_SIZE[1] // 2) - 189))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                pause = False


def main(size) -> None:
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    width, height = size

    pygame.display.set_caption("Прямоугольник")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    screen = pygame.display.set_mode((width, height))
    player = Player(screen, (100, 100), "user_1", obj_type="player", path="player_animations/leaf/")
    # house = House(screen, (500, 300), "house_1", obj_type="player", path="animations/")
    while True:
        # ...
        screen.fill((0,0,0))
        # house.update()
        player.update()
        
        clock.tick(FPS)
        pygame.display.flip()
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player._frame_index = 0
                player._status = "atk2"
                player.give_hit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pause(screen)


if __name__ == '__main__':
    main(WINDOW_SIZE)
