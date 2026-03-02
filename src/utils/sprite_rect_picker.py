import pygame
from pathlib import Path

ASSET = Path("assets/sprites/pacman_general_sprites.png")

def main():
    pygame.init()
    sheet = pygame.image.load(ASSET).convert_alpha()
    screen = pygame.display.set_mode((sheet.get_width(), sheet.get_height()))
    clock = pygame.time.Clock()

    selecting = False
    start = (0, 0)
    rect = pygame.Rect(0, 0, 0, 0)

    print("Maus ziehen = Rect wählen | ENTER = Rect ausgeben | ESC = quit")

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                if e.key == pygame.K_RETURN:
                    print(f"pygame.Rect({rect.x}, {rect.y}, {rect.w}, {rect.h})")
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                selecting = True
                start = e.pos
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                selecting = False
            elif e.type == pygame.MOUSEMOTION and selecting:
                x0, y0 = start
                x1, y1 = e.pos
                rect = pygame.Rect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))

        screen.fill((0, 0, 0))
        screen.blit(sheet, (0, 0))
        pygame.draw.rect(screen, (255, 0, 0), rect, 1)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()