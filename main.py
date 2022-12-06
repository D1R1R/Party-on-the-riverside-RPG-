import pygame
from player import Player


WINDOW_SIZE = (1000, 600)
FPS = 100
RED = (255, 0, 0)

def main(size) -> None:
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    width, height = size

    pygame.display.set_caption("Прямоугольник")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    screen = pygame.display.set_mode((width, height))
    player = Player(screen, (100, 100), "user_1", obj_type="player", path="animations/")
    while True:
        # ...
        player.update()
        
        clock.tick(FPS)
        pygame.display.flip()
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    main(WINDOW_SIZE)
