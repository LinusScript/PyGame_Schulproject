import pygame
from Ghost import Ghost, load_ghost_anims

# =========================
# Pygame Setup
# =========================
pygame.init()
SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Dummy Wall-Collision-Funktion
def wall_collides_fn(rect):
    # Hier einfach innerhalb des Bildschirms bleiben
    return not screen.get_rect().contains(rect)

# =========================
# Ghosts Laden
# =========================
anims_red = load_ghost_anims("red")
anims_blue = load_ghost_anims("blue")
anims_pink = load_ghost_anims("pink")
anims_orange = load_ghost_anims("orange")

ghost_red = Ghost("red", anims_red, (100, 100))
ghost_blue = Ghost("blue", anims_blue, (200, 100))
ghost_pink = Ghost("pink", anims_pink, (100, 200))
ghost_orange = Ghost("orange", anims_orange, (200, 200))

ghosts = pygame.sprite.Group(ghost_red, ghost_blue, ghost_pink, ghost_orange)

# =========================
# Main Loop
# =========================
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta-Time in Sekunden

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ghosts updaten
    ghosts.update(dt, wall_collides_fn)

    # Bildschirm löschen
    screen.fill((0, 0, 0))

    # Ghosts zeichnen
    for ghost in ghosts:
        screen.blit(ghost.image, ghost.rect)

    pygame.display.flip()

pygame.quit()