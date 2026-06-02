import pygame
import sys
from src.core.game import Game
from src.core.settings import Settings


def main():
    pygame.init()
    pygame.mixer.init()

    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
        pygame.RESIZABLE
    )
    pygame.display.set_caption("Balloon Roguelite")
    clock = pygame.time.Clock()

    game = Game(screen, settings, clock)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
