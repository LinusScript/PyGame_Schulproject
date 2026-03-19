def load_gif_frames(path: str):
    frames = []
    gif = Image.open(path)

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            data = frame.tobytes()
            size = frame.size

            py_image = pygame.image.fromstring(data, size, "RGBA")
            py_image = py_image.convert_alpha()

            frames.append(py_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames

def load_ghost_anims(color: str):
    return {
        "left": load_gif_frames(f"assets/{color}_left.gif"),
        "right": load_gif_frames(f"assets/{color}_right.gif"),
        "up": load_gif_frames(f"assets/{color}_up.gif"),
        "down": load_gif_frames(f"assets/{color}_down.gif"),
    }

anims_red = load_ghost_anims("red")
anims_blue = load_ghost_anims("blue")
anims_pink = load_ghost_anims("pink")
anims_orange = load_ghost_anims("orange")

ghost_red = Ghost(anims_red, (100, 100))
ghost_blue = Ghost(anims_blue, (200, 100))
ghost_pink = Ghost(anims_pink, (100, 200))
ghost_orange = Ghost(anims_orange, (200, 200))

ghost_red.update(dt, wall_collides_fn)
ghost_blue.update(dt, wall_collides_fn)
ghost_pink.update(dt, wall_collides_fn)
ghost_orange.update(dt, wall_collides_fn)

screen.blit(ghost_red.image, ghost_red.rect)
screen.blit(ghost_blue.image, ghost_blue.rect)
screen.blit(ghost_pink.image, ghost_pink.rect)
screen.blit(ghost_orange.image, ghost_orange.rect)