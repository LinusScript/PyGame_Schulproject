# src/settings.py
"""
Zentrale Konfiguration für das Pac-Man Projekt.
"""

TITLE = "Pac-Man (Schulprojekt)"
FPS = 60

# Grid / Tiles
TILE = 24
GRID_W = 28
GRID_H = 31

WIDTH = GRID_W * TILE
HEIGHT = GRID_H * TILE

# Gameplay
PAC_SPEED_TPS = 8.0  # Tiles pro Sekunde

# Farben
BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
BLUE = (0, 0, 180)
YELLOW = (255, 220, 0)

#setting Test run