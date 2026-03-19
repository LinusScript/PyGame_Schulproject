# Test
# Update von Code für Git

import importlib
import sys


def load_play_main():
    candidates = ["play", "src.play", "src.states.play"]

    for module_name in candidates:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

        play_main = getattr(module, "main", None)
        if callable(play_main):
            return play_main

    raise ImportError(
        "Es konnte keine main()-Funktion in play.py oder src/play.py gefunden werden."
    )


def main() -> int:
    try:
        play_main = load_play_main()
        play_main()
        return 0
    except Exception as exc:
        print(f"Fehler beim Starten des Spiels: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())