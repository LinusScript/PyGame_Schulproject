import pygame
import random

Vec2 = pygame.math.Vector2

class Ghost(pygame.sprite.Sprite):
    def __init__(self, anims: dict[str, list[pygame.Surface]], center_px: tuple[int, int], speed: float = 120.0):
        super().__init__()
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
            c = self.rect.center
            self.image = self.frames[0]
            self.rect = self.image.get_rect(center=c)

    def update(self, dt: float, wall_collides_fn):
        # simple random-ish movement: if collision -> pick new direction
        step = self.vel * self.speed * dt

        self.rect.x += int(step.x)
        if wall_collides_fn(self.rect):
            self.rect.x -= int(step.x)
            self._pick_new_dir()

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
            c = self.rect.center
            self.image = self.frames[self.frame_i]
            self.rect = self.image.get_rect(center=c)

    def _pick_new_dir(self):
        dirs = [("left", Vec2(-1, 0)), ("right", Vec2(1, 0)), ("up", Vec2(0, -1)), ("down", Vec2(0, 1))]
        d, v = random.choice(dirs)
        self.set_dir(d)
        self.vel = v