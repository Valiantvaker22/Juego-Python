"""
AssetManager - Centralized loader and cache for all game assets.
Falls back to procedurally generated placeholders when files are missing.
"""

import pygame
import os
from src.core.settings import Settings


class AssetManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._images: dict[str, pygame.Surface] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._fonts:  dict[tuple, pygame.font.Font] = {}

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------
    def get_image(self, key: str, size: tuple = None) -> pygame.Surface:
        cache_key = f"{key}_{size}" if size else key
        if cache_key not in self._images:
            path = os.path.join(self.settings.ASSETS_DIR, "images", f"{key}.png")
            if os.path.exists(path):
                surf = pygame.image.load(path).convert_alpha()
            else:
                surf = self._make_placeholder(key, size or (64, 64))
            if size:
                surf = pygame.transform.smoothscale(surf, size)
            self._images[cache_key] = surf
        return self._images[cache_key]

    def _make_placeholder(self, key: str, size: tuple) -> pygame.Surface:
        """Generate a colored placeholder based on asset type."""
        color_map = {
            "balloon": self.settings.RED,
            "tower":   self.settings.GREEN,
            "proj":    self.settings.YELLOW,
            "ui":      self.settings.UI_ACCENT,
        }
        color = next(
            (v for k, v in color_map.items() if k in key),
            self.settings.WHITE
        )
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, color, surf.get_rect())
        return surf

    # ------------------------------------------------------------------
    # Sounds
    # ------------------------------------------------------------------
    def get_sound(self, key: str) -> pygame.mixer.Sound | None:
        if key not in self._sounds:
            path = os.path.join(self.settings.ASSETS_DIR, "sounds", "sfx", f"{key}.wav")
            if os.path.exists(path):
                self._sounds[key] = pygame.mixer.Sound(path)
            else:
                return None
        return self._sounds[key]

    def play(self, key: str, volume: float = 0.6):
        snd = self.get_sound(key)
        if snd:
            snd.set_volume(volume)
            snd.play()

    # ------------------------------------------------------------------
    # Fonts
    # ------------------------------------------------------------------
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:
        cache_key = (size, bold)
        if cache_key not in self._fonts:
            path = os.path.join(self.settings.ASSETS_DIR, "fonts", "game_font.ttf")
            if os.path.exists(path):
                self._fonts[cache_key] = pygame.font.Font(path, size)
            else:
                self._fonts[cache_key] = pygame.font.SysFont("monospace", size, bold=bold)
        return self._fonts[cache_key]
