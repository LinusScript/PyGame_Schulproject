import pygame
import random
from pygame.math import Vector2 as Vec2
from PIL import Image


# =========================
# GIF → Frames
# =========================
def load_gif_frames(path: str) -> list[pygame.Surface]:
    frames = []
    gif = Image.open(path)

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            data = frame.tobytes()
            size = frame.size

            py_image = pygame.image.fromstring(data, size, "RGBA")
            py_image = py_image.convert_alpha()
            py_image = pygame.transform.scale(py_image, (32, 32))

            frames.append(py_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames


# =========================
# Ghost Animation Loader
# =========================
def load_ghost_anims(color: str):
    return {
        "left": load_gif_frames(f"assets/{color}_left.gif"),
        "right": load_gif_frames(f"assets/{color}_right.gif"),
        "up": load_gif_frames(f"assets/{color}_up.gif"),
        "down": load_gif_frames(f"assets/{color}_down.gif"),
    }


# =========================
# Ghost Klasse
# =========================
class Ghost(pygame.sprite.Sprite):
    def __init__(self, color: str, anims, center_px, speed: float = 120.0):
        super().__init__()

        self.color = color
        self.anims = anims

        self.dir = "left"
        self.frames = self.anims[self.dir]

        self.frame_i = 0
        self.anim_t = 0.0
        self.anim_fps = 10.0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center_px)

        self.vel = Vec2(-1, 0)
        self.speed = speed

    def set_dir(self, d: str):
        if d != self.dir:
            self.dir = d
            self.frames = self.anims[self.dir]
            self.frame_i = 0
            self.anim_t = 0.0

            center = self.rect.center
            self.image = self.frames[0]
            self.rect = self.image.get_rect(center=center)

    def update(self, dt: float, wall_collides_fn):
        step = self.vel * self.speed * dt

        # X Bewegung
        self.rect.x += int(step.x)
        if wall_collides_fn(self.rect):
            self.rect.x -= int(step.x)
            self._pick_new_dir()

        # Y Bewegung
        self.rect.y += int(step.y)
        if wall_collides_fn(self.rect):
            self.rect.y -= int(step.y)
            self._pick_new_dir()

        # Animation
        self.anim_t += dt
        frame_step = 1.0 / self.anim_fps

        while self.anim_t >= frame_step:
            self.anim_t -= frame_step
            self.frame_i = (self.frame_i + 1) % len(self.frames)

            center = self.rect.center
            self.image = self.frames[self.frame_i]
            self.rect = self.image.get_rect(center=center)

    def _pick_new_dir(self):
        dirs = [
            ("left", Vec2(-1, 0)),
            ("right", Vec2(1, 0)),
            ("up", Vec2(0, -1)),
            ("down", Vec2(0, 1)),
        ]

        d, v = random.choice(dirs)
        self.set_dir(d)
        self.vel = v


# =========================
# Ghosts erstellen
# =========================
def create_ghosts():
    anims_red = load_ghost_anims("red")
    anims_blue = load_ghost_anims("blue")
    anims_pink = load_ghost_anims("pink")
    anims_orange = load_ghost_anims("orange")

    ghosts = pygame.sprite.Group()

    ghosts.add(
        Ghost("red", anims_red, (100, 100)),
        Ghost("blue", anims_blue, (200, 100)),
        Ghost("pink", anims_pink, (100, 200)),
        Ghost("orange", anims_orange, (200, 200)),
    )

    return ghosts