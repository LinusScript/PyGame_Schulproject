import importlib
from typing import Callable

import pygame


DEFAULT_WIDTH = 672
DEFAULT_HEIGHT = 744
DEFAULT_TITLE = "Pac-Man"


def load_settings() -> tuple[int, int, str]:
    candidates = ["src.settings", "settings"]

    for module_name in candidates:
        try:
            module = importlib.import_module(module_name)
            width = getattr(module, "WIDTH", DEFAULT_WIDTH)
            height = getattr(module, "HEIGHT", DEFAULT_HEIGHT)
            title = getattr(module, "TITLE", DEFAULT_TITLE)
            return width, height, title
        except ModuleNotFoundError:
            continue

    return DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_TITLE


def load_menu_class():
    candidates = ["menu", "src.menu", "src.states.menu"]

    for module_name in candidates:
        try:
            module = importlib.import_module(module_name)
            menu_class = getattr(module, "MainMenu", None)
            if menu_class is not None:
                return menu_class
        except ModuleNotFoundError:
            continue

    raise ImportError("MainMenu konnte nicht gefunden werden.")


def build_game_runner(screen: pygame.Surface) -> Callable[[], None]:
    module_candidates = ["src.game", "game", "src.states.game"]

    for module_name in module_candidates:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

        game_class = getattr(module, "Game", None)
        if game_class is not None:
            def run_game_from_class(module_game_class=game_class) -> None:
                game = None

                for args in ((screen,), tuple()):
                    try:
                        game = module_game_class(*args)
                        break
                    except TypeError:
                        continue

                if game is None:
                    raise TypeError("Game konnte nicht erzeugt werden.")

                for method_name in ("run", "start", "play"):
                    method = getattr(game, method_name, None)
                    if callable(method):
                        method()
                        return

                raise AttributeError("Game hat keine passende Startmethode (run/start/play).")

            return run_game_from_class

        for function_name in ("main", "run", "start_game", "play"):
            function = getattr(module, function_name, None)
            if callable(function):
                def run_game_from_function(module_function=function) -> None:
                    try:
                        module_function(screen)
                    except TypeError:
                        module_function()

                return run_game_from_function

    raise ImportError("Es wurde keine Game-Klasse oder Startfunktion gefunden.")


def main() -> None:
    pygame.init()

    width, height, title = load_settings()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    menu_class = load_menu_class()
    run_game = build_game_runner(screen)

    running = True
    while running:
        menu = menu_class(screen, title=title)
        action = menu.run()

        if action == "start":
            run_game()
            if not pygame.get_init():
                pygame.init()
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
        else:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()