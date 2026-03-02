import pygame

class Pellet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, center_px: tuple[int, int]):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center_px)