from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple
"""level.py

A clean, tile-based level implementation for a Pac-Man style game.

Goals:
- Simple map format (ASCII grid)
- Fast collision checks (precomputed wall rects)
- Pellet + power-pellet handling
- Nice looking rendering (rounded walls, crisp pellets)

Map legend:
  #  = wall
  .  = pellet
  o  = power pellet
  P  = player spawn
  G  = ghost spawn (can appear multiple times)
  ' ' or any other char = empty

If no external map file is found, a built-in default map is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple

import pygame


# --- Settings import (robust) -------------------------------------------------
# This keeps the project running even while you refactor settings.
try:
    import settings as S

    TILE: int = getattr(S, "TILE", 24)
    BLACK = getattr(S, "BLACK", (0, 0, 0))
    WHITE = getattr(S, "WHITE", (240, 240, 240))
    BLUE = getattr(S, "BLUE", (0, 0, 180))
    YELLOW = getattr(S, "YELLOW", (255, 220, 0))

    # Optional: allow a map path or inline level from settings
    LEVEL_PATH = getattr(S, "LEVEL_PATH", None)
    LEVEL_MAP = getattr(S, "LEVEL_MAP", None)
except Exception:  # pragma: no cover
    TILE = 24
    BLACK = (0, 0, 0)
    WHITE = (240, 240, 240)
    BLUE = (0, 0, 180)
    YELLOW = (255, 220, 0)
    LEVEL_PATH = None
    LEVEL_MAP = None


Vec2 = pygame.math.Vector2
GridPos = Tuple[int, int]


DEFAULT_MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##### ## #####.#     ",
    "     #.##          ##.#     ",
    "     #.## ###GG### ##.#     ",
    "######.## #      # ##.######",
    "      .   #  PP  #   .      ",
    "######.## #      # ##.######",
    "     #.## ######## ##.#     ",
    "     #.##          ##.#     ",
    "     #.## ######## ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


@dataclass(frozen=True)
class Spawns:
    player: GridPos
    ghosts: Tuple[GridPos, ...]


class Level:
    """Holds level map, collisions, pellets, and rendering."""

    def __init__(
        self,
        map_lines: Optional[Sequence[str]] = None,
        map_path: Optional[str | Path] = None,
        tile_size: int = TILE,
    ) -> None:
        self.tile = int(tile_size)

        # Load map
        self.lines: List[str] = self._load_map(map_lines=map_lines, map_path=map_path)

        self.height = len(self.lines)
        self.width = max(len(r) for r in self.lines) if self.height else 0

        # Normalize: right-pad lines to equal length
        self.lines = [row.ljust(self.width) for row in self.lines]

        # Precompute
        self.walls: List[pygame.Rect] = []
        self.pellets: Set[GridPos] = set()
        self.power_pellets: Set[GridPos] = set()
        self.spawn_player: GridPos = (1, 1)
        self.spawn_ghosts: List[GridPos] = []

        self._parse_map()
        self._build_wall_rects()

        # Cached surfaces for prettier rendering
        self._wall_surface = pygame.Surface(self.pixel_size, pygame.SRCALPHA)
        self._redraw_walls()

    # ------------------------------ Loading ---------------------------------

    def _load_map(
        self,
        map_lines: Optional[Sequence[str]],
        map_path: Optional[str | Path],
    ) -> List[str]:
        # Priority: explicit args -> settings LEVEL_MAP -> settings LEVEL_PATH -> default file -> built-in default
        if map_lines:
            return [str(x).rstrip("\n") for x in map_lines]

        if isinstance(LEVEL_MAP, (list, tuple)) and LEVEL_MAP:
            return [str(x).rstrip("\n") for x in LEVEL_MAP]

        candidate: Optional[Path] = None
        if map_path is not None:
            candidate = Path(map_path)
        elif LEVEL_PATH:
            candidate = Path(LEVEL_PATH)
        else:
            # Common default location
            candidate = Path("assets") / "maps" / "level1.txt"

        try:
            if candidate and candidate.exists():
                return candidate.read_text(encoding="utf-8").splitlines()
        except Exception:
            pass

        return list(DEFAULT_MAP)

    # ------------------------------ Parsing ---------------------------------

    def _parse_map(self) -> None:
        for y, row in enumerate(self.lines):
            for x, ch in enumerate(row):
                if ch == "#":
                    # walls handled in _build_wall_rects
                    continue
                if ch == ".":
                    self.pellets.add((x, y))
                elif ch == "o":
                    self.power_pellets.add((x, y))
                elif ch == "P":
                    self.spawn_player = (x, y)
                elif ch == "G":
                    self.spawn_ghosts.append((x, y))

        # Fallback spawns if map didn't define them
        if not self.spawn_ghosts:
            self.spawn_ghosts = [(self.width // 2, self.height // 2)]

    def _build_wall_rects(self) -> None:
        """Build a rect per wall-tile (fast + simple)."""
        t = self.tile
        self.walls.clear()
        for y, row in enumerate(self.lines):
            for x, ch in enumerate(row):
                if ch == "#":
                    self.walls.append(pygame.Rect(x * t, y * t, t, t))

    # ------------------------------ Public API ------------------------------

    @property
    def pixel_size(self) -> Tuple[int, int]:
        return self.width * self.tile, self.height * self.tile

    @property
    def spawns(self) -> Spawns:
        return Spawns(player=self.spawn_player, ghosts=tuple(self.spawn_ghosts))

    def grid_to_pixel_center(self, pos: GridPos) -> Tuple[int, int]:
        x, y = pos
        return (x * self.tile + self.tile // 2, y * self.tile + self.tile // 2)

    def pixel_to_grid(self, px: float, py: float) -> GridPos:
        return int(px) // self.tile, int(py) // self.tile

    def in_bounds_grid(self, pos: GridPos) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall_grid(self, pos: GridPos) -> bool:
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            return True
        return self.lines[y][x] == "#"

    def rect_collides_walls(self, rect: pygame.Rect) -> bool:
        # Cheap broad-phase: only test nearby walls
        # Compute a small search area in tile coords
        t = self.tile
        gx0 = max(0, rect.left // t - 1)
        gx1 = min(self.width - 1, rect.right // t + 1)
        gy0 = max(0, rect.top // t - 1)
        gy1 = min(self.height - 1, rect.bottom // t + 1)

        for gy in range(gy0, gy1 + 1):
            row = self.lines[gy]
            for gx in range(gx0, gx1 + 1):
                if row[gx] == "#":
                    wall_rect = pygame.Rect(gx * t, gy * t, t, t)
                    if rect.colliderect(wall_rect):
                        return True
        return False

    def eat_at_pixel(self, px: float, py: float) -> Tuple[bool, bool]:
        """Try to eat a pellet at pixel location.

        Returns:
            (ate_pellet, ate_power_pellet)
        """
        gp = self.pixel_to_grid(px, py)
        if gp in self.pellets:
            self.pellets.remove(gp)
            return True, False
        if gp in self.power_pellets:
            self.power_pellets.remove(gp)
            return False, True
        return False, False

    def remaining_pellets(self) -> int:
        return len(self.pellets) + len(self.power_pellets)

    # ------------------------------ Rendering -------------------------------

    def _redraw_walls(self) -> None:
        """Draw all walls once to a cached surface for smooth visuals."""
        surf = self._wall_surface
        surf.fill((0, 0, 0, 0))

        t = self.tile
        # Soft inner padding to show separation between tiles
        pad = max(1, t // 10)
        radius = max(2, t // 4)

        for y, row in enumerate(self.lines):
            for x, ch in enumerate(row):
                if ch != "#":
                    continue
                r = pygame.Rect(x * t + pad, y * t + pad, t - 2 * pad, t - 2 * pad)
                pygame.draw.rect(surf, BLUE, r, border_radius=radius)

                # simple highlight for a more "arcade" look
                highlight = pygame.Rect(r.x + 2, r.y + 2, r.w - 4, r.h - 4)
                pygame.draw.rect(surf, (min(255, BLUE[0] + 30), min(255, BLUE[1] + 30), min(255, BLUE[2] + 30)),
                                 highlight, width=2, border_radius=max(2, radius - 2))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw background, walls, pellets."""
        # Background
        screen.fill(BLACK)

        # Walls
        screen.blit(self._wall_surface, (0, 0))

        # Pellets
        t = self.tile
        pellet_r = max(2, t // 10)
        power_r = max(4, t // 4)

        for (x, y) in self.pellets:
            cx, cy = x * t + t // 2, y * t + t // 2
            pygame.draw.circle(screen, WHITE, (cx, cy), pellet_r)

        for (x, y) in self.power_pellets:
            cx, cy = x * t + t // 2, y * t + t // 2
            pygame.draw.circle(screen, WHITE, (cx, cy), power_r)

    # ------------------------------ Debug -----------------------------------



    def debug_draw_grid(self, screen: pygame.Surface, color: Tuple[int, int, int] = (40, 40, 40)) -> None:
        """Optional: draw a light grid overlay for debugging."""
        w, h = self.pixel_size
        t = self.tile
        for x in range(0, w + 1, t):
            pygame.draw.line(screen, color, (x, 0), (x, h))
        for y in range(0, h + 1, t):
            pygame.draw.line(screen, color, (0, y), (w, y))

import pygame



try:
    import settings as S

    TILE: int = getattr(S, "TILE",24)
    BLACK = getattr(S, "BLACK", (0, 0, 0))
    WHITE = getattr(S, "WHITE", (240, 240, 240))
    BLUE = getattr(S,"BLUE", (0,0,180))
    YELLOW = getattr(S,"YELLOW", (240,255,0))

        LEVEL_PATH = getattr(S,"LEVEL_PATH",None)
            LEVEL_MAP