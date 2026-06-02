"""
BalloonFactory - Creates balloon instances from registered definitions.
"""

import pygame
from typing import List, Tuple
from src.entities.balloons.balloon import Balloon, BalloonDef


# -----------------------------------------------------------------------
# Built-in balloon type registry
# (in a real game these come from data/balloons.json)
# -----------------------------------------------------------------------
_REGISTRY: dict[str, BalloonDef] = {
    "red": BalloonDef(
        id="red", name="Red Balloon", hp=1, speed=120, rbe=1, reward=1,
        color=(220, 50, 50), children=[]
    ),
    "blue": BalloonDef(
        id="blue", name="Blue Balloon", hp=1, speed=150, rbe=2, reward=1,
        color=(60, 110, 220), children=["red"]
    ),
    "green": BalloonDef(
        id="green", name="Green Balloon", hp=1, speed=180, rbe=3, reward=1,
        color=(50, 190, 80), children=["blue"]
    ),
    "yellow": BalloonDef(
        id="yellow", name="Yellow Balloon", hp=1, speed=280, rbe=4, reward=2,
        color=(240, 220, 40), children=["green"]
    ),
    "pink": BalloonDef(
        id="pink", name="Pink Balloon", hp=1, speed=350, rbe=5, reward=2,
        color=(240, 100, 180), children=["yellow"]
    ),
    "black": BalloonDef(
        id="black", name="Black Balloon", hp=1, speed=180, rbe=11, reward=5,
        color=(40, 40, 40), children=["pink", "pink"],
        immune_to=["explosive"]
    ),
    "white": BalloonDef(
        id="white", name="White Balloon", hp=1, speed=200, rbe=11, reward=5,
        color=(230, 230, 230), children=["pink", "pink"],
        immune_to=["freeze"]
    ),
    "lead": BalloonDef(
        id="lead", name="Lead Balloon", hp=1, speed=100, rbe=23, reward=8,
        color=(120, 130, 140), children=["black", "black"],
        immune_to=["sharp"], size=40
    ),
    "zebra": BalloonDef(
        id="zebra", name="Zebra Balloon", hp=1, speed=180, rbe=23, reward=8,
        color=(180, 180, 180), children=["black", "white"],
        immune_to=["explosive", "freeze"], size=40
    ),
    "rainbow": BalloonDef(
        id="rainbow", name="Rainbow Balloon", hp=1, speed=220, rbe=47, reward=15,
        color=(200, 100, 220), children=["zebra", "zebra"], size=44
    ),
    "ceramic": BalloonDef(
        id="ceramic", name="Ceramic Balloon", hp=10, speed=250, rbe=104, reward=30,
        color=(200, 160, 100), children=["rainbow", "rainbow"], size=48
    ),
    "moab": BalloonDef(
        id="moab", name="MOAB", hp=200, speed=60, rbe=616, reward=100,
        color=(60, 80, 160), children=["ceramic"] * 4, size=80
    ),
    "bfb": BalloonDef(
        id="bfb", name="BFB", hp=700, speed=25, rbe=3164, reward=500,
        color=(20, 30, 80), children=["moab"] * 4, size=100
    ),
}


class BalloonFactory:
    @staticmethod
    def spawn(
        balloon_id: str,
        path: List[Tuple[float, float]],
        speed_scale: float = 1.0,
        start_wp: int = 0,
        start_pos: pygame.math.Vector2 = None,
    ) -> Balloon:
        defn = _REGISTRY.get(balloon_id)
        if defn is None:
            raise ValueError(f"Unknown balloon id: '{balloon_id}'")

        balloon = Balloon(defn, path, speed_scale)
        if start_pos:
            balloon.pos = pygame.math.Vector2(start_pos)
            balloon._wp_index = max(1, start_wp + 1)
            balloon.rect.center = (int(balloon.pos.x), int(balloon.pos.y))
        return balloon

    @staticmethod
    def register(defn: BalloonDef):
        _REGISTRY[defn.id] = defn

    @staticmethod
    def get_def(balloon_id: str) -> BalloonDef:
        return _REGISTRY[balloon_id]

    @staticmethod
    def all_ids() -> list[str]:
        return list(_REGISTRY.keys())
