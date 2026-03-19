import pygame
from src.level import Level

pygame.init()

level = Level()
screen = pygame.display.set_mode(level.pixel_size)
pygame.display.set_caption("Level Vorschau")

clock = pygame.time.Clock()
running = True
show_grid = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_g:
                show_grid = not show_grid

    level.draw(screen)

    if show_grid:
        level.debug_draw_grid(screen)

    pygame.display.flip()

pygame.quit()