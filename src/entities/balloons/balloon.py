"""
Balloon - Base entity. Follows a waypoint path.
"""

import pygame
import math
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class BalloonDef:
    """Definition (data) for a balloon type - loaded from JSON."""
    id:          str
    name:        str
    hp:          int          # layers / hit points
    speed:       float        # pixels per second at scale 1.0
    rbe:         int          # Red Balloon Equivalent (power metric)
    reward:      int          # gold on pop
    color:       Tuple[int,int,int] = (220, 50, 50)
    children:    List[str] = field(default_factory=list)  # ids spawned on pop
    immune_to:   List[str] = field(default_factory=list)  # e.g. ["sharp", "fire"]
    size:        int = 32


class Balloon(pygame.sprite.Sprite):
    def __init__(self, defn: BalloonDef, path: List[Tuple[float,float]], speed_scale: float = 1.0):
        super().__init__()
        self.defn        = defn
        self.path        = path
        self.speed_scale = speed_scale

        self.hp          = defn.hp
        self.speed       = defn.speed * speed_scale
        self.alive_flag  = True
        self.reached_end = False

        # path traversal
        self._wp_index   = 1          # target waypoint
        self._distance   = 0.0        # total distance traveled (for sorting)
        self.pos         = pygame.math.Vector2(path[0])

        # sprite
        self.image = pygame.Surface((defn.size, defn.size), pygame.SRCALPHA)
        self._draw_self()
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    # ------------------------------------------------------------------
    def _draw_self(self):
        """Procedural balloon shape (replaced when real assets load)."""
        s = self.defn.size
        self.image.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.image, self.defn.color, (0, 2, s, s - 4))
        # shine
        pygame.draw.ellipse(self.image, (255, 255, 255, 80),
                            (s//4, s//6, s//4, s//5))

    def update(self, dt: float):
        if not self.alive_flag or self._wp_index >= len(self.path):
            return

        target = pygame.math.Vector2(self.path[self._wp_index])
        direction = target - self.pos
        dist_to_target = direction.length()
        move = self.speed * dt

        if move >= dist_to_target:
            self.pos = target
            self._distance += dist_to_target
            self._wp_index += 1
            if self._wp_index >= len(self.path):
                self.reached_end = True
                self.kill()
        else:
            self.pos += direction.normalize() * move
            self._distance += move

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    # ------------------------------------------------------------------
    def take_damage(self, amount: int, damage_type: str = "sharp") -> list["Balloon"]:
        """
        Apply damage. Returns list of child balloons spawned on pop.
        Respects immunities.
        """
        if damage_type in self.defn.immune_to:
            return []

        self.hp -= amount
        if self.hp <= 0:
            return self._pop()
        return []

    def _pop(self) -> list["Balloon"]:
        self.alive_flag = False
        self.kill()
        children = []
        for child_id in self.defn.children:
            # BalloonFactory resolves child_id -> BalloonDef
            # imported here to avoid circular dep
            from src.entities.balloons.balloon_factory import BalloonFactory
            child = BalloonFactory.spawn(child_id, self.path,
                                         self.speed_scale, start_wp=self._wp_index - 1,
                                         start_pos=self.pos)
            children.append(child)
        return children

    @property
    def distance_traveled(self) -> float:
        return self._distance
