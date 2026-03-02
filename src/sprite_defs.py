import pygame
from pathlib import Path
from src.spritesheet import SpriteSheet

SPRITE_PATH = Path("assets/sprites/pacman_general_sprites.png")

# ⚠️ Diese Rects musst du mit dem Rect-Picker eintragen:
RECTS = {
    # Pac-Man (2 Frames je Richtung)
    "pac_right_0": pygame.Rect(0, 0, 0, 0),
    "pac_right_1": pygame.Rect(0, 0, 0, 0),
    "pac_left_0":  pygame.Rect(0, 0, 0, 0),
    "pac_left_1":  pygame.Rect(0, 0, 0, 0),
    "pac_up_0":    pygame.Rect(0, 0, 0, 0),
    "pac_up_1":    pygame.Rect(0, 0, 0, 0),
    "pac_down_0":  pygame.Rect(0, 0, 0, 0),
    "pac_down_1":  pygame.Rect(0, 0, 0, 0),

    # Ghost (2 Frames je Richtung)
    "ghost_left_0":  pygame.Rect(0, 0, 0, 0),
    "ghost_left_1":  pygame.Rect(0, 0, 0, 0),
    "ghost_right_0": pygame.Rect(0, 0, 0, 0),
    "ghost_right_1": pygame.Rect(0, 0, 0, 0),
    "ghost_up_0":    pygame.Rect(0, 0, 0, 0),
    "ghost_up_1":    pygame.Rect(0, 0, 0, 0),
    "ghost_down_0":  pygame.Rect(0, 0, 0, 0),
    "ghost_down_1":  pygame.Rect(0, 0, 0, 0),

    # Pellets
    "pellet": pygame.Rect(0, 0, 0, 0),
    "power":  pygame.Rect(0, 0, 0, 0),
}

def load_sprites(tile_size: int = 24):
    sheet = SpriteSheet(str(SPRITE_PATH))

    def frame(name: str) -> pygame.Surface:
        return sheet.get(RECTS[name], scale_to=(tile_size, tile_size))

    pacman_anims = {
        "right": [frame("pac_right_0"), frame("pac_right_1")],
        "left":  [frame("pac_left_0"), frame("pac_left_1")],
        "up":    [frame("pac_up_0"), frame("pac_up_1")],
        "down":  [frame("pac_down_0"), frame("pac_down_1")],
    }

    ghost_anims = {
        "left":  [frame("ghost_left_0"), frame("ghost_left_1")],
        "right": [frame("ghost_right_0"), frame("ghost_right_1")],
        "up":    [frame("ghost_up_0"), frame("ghost_up_1")],
        "down":  [frame("ghost_down_0"), frame("ghost_down_1")],
    }

    pellet_img = sheet.get(RECTS["pellet"], scale_to=(tile_size // 3, tile_size // 3))
    power_img  = sheet.get(RECTS["power"],  scale_to=(tile_size // 2, tile_size // 2))

    return pacman_anims, ghost_anims, pellet_img, power_img