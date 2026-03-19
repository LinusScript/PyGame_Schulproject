import pygame
import random
from pygame.math import Vector2 as Vec2
from PIL import Image

# =========================
# GIF → Frames
# =========================
def load_gif_frames(path: str, scale: tuple[int, int] = (32, 32)) -> list[pygame.Surface]:
    frames = []
    gif = Image.open(path)

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            data = frame.tobytes()
            size = frame.size

            py_image = pygame.image.fromstring(data, size, "RGBA")
            py_image = py_image.convert_alpha()
            py_image = pygame.transform.scale(py_image, scale)

            frames.append(py_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames

# =========================
# Ghost Animation Loader
# =========================
def load_ghost_anims(color: str, scale: tuple[int, int] = (32, 32)):
    return {
        "left": load_gif_frames(f"assets/{color}_left.gif", scale),
        "right": load_gif_frames(f"assets/{color}_right.gif", scale),
        "up": load_gif_frames(f"assets/{color}_up.gif", scale),
        "down": load_gif_frames(f"assets/{color}_down.gif", scale),
    }

# =========================
# Ghost Klasse
# =========================
class Ghost(pygame.sprite.Sprite):
    def __init__(self, color: str, anims, center_px, speed: float = 120.0, anim_fps: float = 10.0):
        super().__init__()

        self.color = color
        self.anims = anims
        self.speed = speed
        self.anim_fps = anim_fps

        # Anfangsrichtung
        self.dir = "left"
        self.frames = self.anims[self.dir]
        self.frame_i = 0
        self.anim_t = 0.0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center_px)

        self.vel = Vec2(-1, 0)

    # Richtung wechseln
    def set_dir(self, d: str):
        if d != self.dir:
            self.dir = d
            self.frames = self.anims[self.dir]
            self.frame_i = 0
            self.anim_t = 0.0

            center = self.rect.center
            self.image = self.frames[0]
            self.rect = self.image.get_rect(center=center)

    # Update pro Frame
    def update(self, dt: float, wall_collides_fn):
        step = self.vel * self.speed * dt

        # X-Bewegung
        self.rect.x += int(step.x)
        if wall_collides_fn(self.rect):
            self.rect.x -= int(step.x)
            self._pick_new_dir()

        # Y-Bewegung
        self.rect.y += int(step.y)
        if wall_collides_fn(self.rect):
            self.rect.y -= int(step.y)
            self._pick_new_dir()

        # Animation aktualisieren
        self.anim_t += dt
        frame_step = 1.0 / self.anim_fps

        while self.anim_t >= frame_step:
            self.anim_t -= frame_step
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_i]
            self.rect = self.image.get_rect(center=center)

    # Zufällige neue Richtung wählen
    def _pick_new_dir(self):
        dirs = [
            ("left", Vec2(-1, 0)),
            ("right", Vec2(1, 0)),
            ("up", Vec2(0, -1)),
            ("down", Vec2(0, 1)),
        ]

        # Rückwärtsrichtung vermeiden
        opposite = {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up"
        }
        dirs = [d for d in dirs if d[0] != opposite[self.dir]]

        d, v = random.choice(dirs)
        self.set_dir(d)
        self.vel = v