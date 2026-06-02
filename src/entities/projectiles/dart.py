"""
Dart - Basic straight-line projectile.
"""

import pygame


class Dart(pygame.sprite.Sprite):
    SPEED = 500  # px/s

    def __init__(
        self,
        origin: pygame.math.Vector2,
        target_pos: pygame.math.Vector2,
        damage: int = 1,
        pierce: int = 1,
        damage_type: str = "sharp",
    ):
        super().__init__()
        self.pos         = pygame.math.Vector2(origin)
        self.damage      = damage
        self.pierce      = pierce
        self.damage_type = damage_type
        self._hits_left  = pierce

        diff = target_pos - origin
        self.velocity = diff.normalize() * self.SPEED if diff.length() > 0 else pygame.math.Vector2(1, 0) * self.SPEED

        self.image = pygame.Surface((12, 4), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (230, 200, 60),
                            [(0, 2), (10, 0), (12, 2), (10, 4)])
        angle = -self.velocity.angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def update(self, dt: float):
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # remove if off-screen (rough bounds)
        if not (-100 < self.pos.x < 2000 and -100 < self.pos.y < 2000):
            self.kill()

    def on_hit(self, balloon) -> list:
        """Called by collision system. Returns child balloons spawned."""
        children = balloon.take_damage(self.damage, self.damage_type)
        self._hits_left -= 1
        if self._hits_left <= 0:
            self.kill()
        return children
