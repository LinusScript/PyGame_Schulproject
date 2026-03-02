import pygame
from src.level import Level
from src.sprite_defs import load_sprites
from src.entities.pacman import Pacman
from src.entities.ghost import Ghost
from src.entities.pellet import Pellet

def main():
    pygame.init()

    level = Level()
    screen = pygame.display.set_mode(level.pixel_size)
    clock = pygame.time.Clock()

    pac_anims, ghost_anims, pellet_img, power_img = load_sprites(tile_size=level.tile)

    pac = Pacman(pac_anims, level.grid_to_pixel_center(level.spawn_player))
    ghosts = [Ghost(ghost_anims, level.grid_to_pixel_center(g)) for g in level.spawn_ghosts]

    pellet_sprites = pygame.sprite.Group()
    for gp in level.pellets:
        pellet_sprites.add(Pellet(pellet_img, level.grid_to_pixel_center(gp)))
    for gp in level.power_pellets:
        pellet_sprites.add(Pellet(power_img, level.grid_to_pixel_center(gp)))

    entity_sprites = pygame.sprite.Group(pac, *ghosts)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        pac.handle_input(keys)

        pac.update(dt, level.rect_collides_walls)
        for g in ghosts:
            g.update(dt, level.rect_collides_walls)

        level.draw(screen)
        pellet_sprites.draw(screen)
        entity_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()