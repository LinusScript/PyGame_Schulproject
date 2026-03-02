import sys
from pathlib import Path

import pygame

# Ensure project root is on sys.path so `import src.*` works when this file is run directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # .../PyGame_Schulproject
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.level import Level  # level.py liegt unter src/

def main():
    pygame.init()

    level = Level()  # nutzt DEFAULT_MAP oder assets/maps/level1.txt (wenn vorhanden)

    screen = pygame.display.set_mode(level.pixel_size)
    pygame.display.set_caption("Level Test")

    clock = pygame.time.Clock()
    show_grid = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_g:
                    show_grid = not show_grid

        level.draw(screen)
        if show_grid:
            level.debug_draw_grid(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()