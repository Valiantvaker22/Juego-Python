"""
Settings - Global constants and configuration
"""

from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Settings:
    # --- Screen ---
    SCREEN_WIDTH: int = 1280
    SCREEN_HEIGHT: int = 720
    FPS: int = 60
    TILE_SIZE: int = 64

    # --- Colors ---
    BLACK:      Tuple = (0,   0,   0)
    WHITE:      Tuple = (255, 255, 255)
    RED:        Tuple = (220, 50,  50)
    GREEN:      Tuple = (50,  200, 80)
    BLUE:       Tuple = (50,  100, 220)
    YELLOW:     Tuple = (240, 220, 50)
    PURPLE:     Tuple = (160, 60,  200)
    ORANGE:     Tuple = (240, 140, 30)
    PINK:       Tuple = (240, 100, 180)
    DARK_BG:    Tuple = (20,  22,  30)
    UI_PANEL:   Tuple = (30,  33,  45)
    UI_ACCENT:  Tuple = (80,  200, 140)

    # --- Game Economy ---
    STARTING_GOLD: int = 150
    STARTING_LIVES: int = 100
    GOLD_PER_POP: int = 1          # gold per balloon popped
    GOLD_PER_ROUND: int = 100      # bonus gold at round end

    # --- Roguelite ---
    MAX_MAP_NODES: int = 15        # nodes per run map
    ELITE_CHANCE: float = 0.15     # probability of elite round
    SHOP_CHANCE: float = 0.20      # probability of shop node
    EVENT_CHANCE: float = 0.10     # probability of random event

    # --- Balloon base stats (scaled per round) ---
    BALLOON_BASE_SPEED: float = 1.0
    BALLOON_SCALE_PER_ROUND: float = 0.05   # +5% speed each round

    # --- Tower limits ---
    MAX_TOWERS_ON_MAP: int = 20

    # --- Paths ---
    ASSETS_DIR: str = "assets"
    DATA_DIR: str = "data"
    SAVES_DIR: str = "saves"
