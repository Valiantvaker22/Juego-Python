"""
DartMonkey - Starter tower. Throws darts at first-in-range balloon.
"""

import pygame
from src.entities.towers.tower import Tower
from src.entities.projectiles.dart import Dart


class DartMonkey(Tower):
    COST        = 200
    NAME        = "Dart Monkey"
    DESCRIPTION = "Throws darts at balloons. Fast and cheap."
    DAMAGE_TYPE = "sharp"

    def __init__(self, grid_x, grid_y, tile_size=64):
        super().__init__(grid_x, grid_y, tile_size)
        self.range_px   = 180
        self.attack_spd = 1.4
        self.pierce     = 1
        self.damage     = 1
        self._redraw()

    def _redraw(self):
        s = self.tile_size
        self.image.fill((0, 0, 0, 0))
        # body
        pygame.draw.circle(self.image, (180, 120, 60), (s//2, s//2), s//3)
        pygame.draw.circle(self.image, (200, 150, 80), (s//2, s//2), s//3, 2)

    def find_target(self, balloon_group):
        return self._first_in_range(balloon_group)

    def shoot(self, target) -> list:
        dart = Dart(
            origin=pygame.math.Vector2(self.world_pos),
            target_pos=pygame.math.Vector2(target.pos),
            damage=self.damage,
            pierce=self.pierce,
            damage_type=self.DAMAGE_TYPE,
        )
        return [dart]
