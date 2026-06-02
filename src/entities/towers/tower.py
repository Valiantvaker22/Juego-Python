"""
Tower - Base class for all towers.
Each subclass overrides `find_target`, `shoot`, and optionally `draw_extra`.
"""

import pygame
import math
from abc import abstractmethod
from src.entities.balloons.balloon import Balloon


class Tower(pygame.sprite.Sprite):
    # Override in subclasses
    COST:        int   = 100
    NAME:        str   = "Base Tower"
    DESCRIPTION: str   = ""
    DAMAGE_TYPE: str   = "sharp"

    def __init__(self, grid_x: int, grid_y: int, tile_size: int = 64):
        super().__init__()
        self.grid_x    = grid_x
        self.grid_y    = grid_y
        self.tile_size = tile_size
        self.world_pos = pygame.math.Vector2(
            grid_x * tile_size + tile_size // 2,
            grid_y * tile_size + tile_size // 2,
        )

        # stats (may be modified by upgrades)
        self.range_px    = 160.0
        self.attack_spd  = 1.0   # attacks per second
        self._cd         = 0.0   # cooldown remaining
        self.pierce      = 1     # balloons hit per projectile
        self.damage      = 1

        # upgrade state
        self.upgrade_path: list[str] = []

        # sprite
        self.image = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        self._draw_base()
        self.rect = self.image.get_rect(topleft=(grid_x * tile_size, grid_y * tile_size))

    # ------------------------------------------------------------------
    def _draw_base(self):
        s = self.tile_size
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, (60, 180, 80), (8, 8, s-16, s-16), border_radius=6)
        pygame.draw.rect(self.image, (80, 220, 100), (8, 8, s-16, s-16), border_radius=6, width=2)

    # ------------------------------------------------------------------
    def update(self, dt: float, balloon_group: pygame.sprite.Group):
        self._cd = max(0.0, self._cd - dt)
        if self._cd <= 0:
            target = self.find_target(balloon_group)
            if target:
                projectiles = self.shoot(target)
                self._cd = 1.0 / self.attack_spd
                return projectiles
        return []

    # ------------------------------------------------------------------
    @abstractmethod
    def find_target(self, balloon_group: pygame.sprite.Group) -> Balloon | None:
        """Return the balloon this tower will aim at."""
        ...

    @abstractmethod
    def shoot(self, target: Balloon) -> list:
        """Create and return projectile(s)."""
        ...

    # ------------------------------------------------------------------
    def _balloons_in_range(self, group: pygame.sprite.Group) -> list[Balloon]:
        in_range = []
        for b in group:
            if self.world_pos.distance_to(b.pos) <= self.range_px:
                in_range.append(b)
        return in_range

    def _first_in_range(self, group: pygame.sprite.Group) -> Balloon | None:
        """Classic BTD targeting: balloon furthest along the path."""
        candidates = self._balloons_in_range(group)
        if not candidates:
            return None
        return max(candidates, key=lambda b: b.distance_traveled)

    # ------------------------------------------------------------------
    def draw_range(self, surface: pygame.Surface):
        pygame.draw.circle(surface, (255, 255, 255, 40),
                           (int(self.world_pos.x), int(self.world_pos.y)),
                           int(self.range_px), 1)
