import pygame

Vec2 = pygame.math.Vector2

class Pacman(pygame.sprite.Sprite):
    def __init__(self, anims: dict[str, list[pygame.Surface]], center_px: tuple[int, int], speed: float = 140.0):
        super().__init__()
        self.anims = anims
        self.dir = "right"
        self.frames = self.anims[self.dir]
        self.frame_i = 0
        self.anim_t = 0.0
        self.anim_fps = 12.0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=center_px)

        self.vel = Vec2(0, 0)
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

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.vel = Vec2(-1, 0); self.set_dir("left")
        elif keys[pygame.K_RIGHT]:
            self.vel = Vec2(1, 0); self.set_dir("right")
        elif keys[pygame.K_UP]:
            self.vel = Vec2(0, -1); self.set_dir("up")
        elif keys[pygame.K_DOWN]:
            self.vel = Vec2(0, 1); self.set_dir("down")
        else:
            self.vel = Vec2(0, 0)

    def update(self, dt: float, wall_collides_fn):
        # Movement
        if self.vel.length_squared() > 0:
            step = self.vel * self.speed * dt

            self.rect.x += int(step.x)
            if wall_collides_fn(self.rect):
                self.rect.x -= int(step.x)

            self.rect.y += int(step.y)
            if wall_collides_fn(self.rect):
                self.rect.y -= int(step.y)

        # Animation
        if self.vel.length_squared() == 0:
            return

        self.anim_t += dt
        frame_step = 1.0 / self.anim_fps
        while self.anim_t >= frame_step:
            self.anim_t -= frame_step
            self.frame_i = (self.frame_i + 1) % len(self.frames)
            c = self.rect.center
            self.image = self.frames[self.frame_i]
            self.rect = self.image.get_rect(center=c)