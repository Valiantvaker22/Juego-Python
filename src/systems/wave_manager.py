"""
WaveManager - Spawns balloons according to a wave definition.
Wave defs come from data/waves.json (or are generated procedurally for roguelite).
"""

import pygame
from src.entities.balloons.balloon_factory import BalloonFactory
from src.entities.balloons.balloon import Balloon


class SpawnEntry:
    def __init__(self, balloon_id: str, count: int, interval: float, delay: float = 0.0):
        self.balloon_id = balloon_id
        self.count      = count
        self.interval   = interval   # seconds between each balloon
        self.delay      = delay      # seconds before first spawn


class WaveManager:
    def __init__(self, path, speed_scale: float, balloon_group: pygame.sprite.Group):
        self.path          = path
        self.speed_scale   = speed_scale
        self.balloon_group = balloon_group

        self._queue: list[SpawnEntry] = []
        self._active: list[dict]      = []   # running spawn streams
        self._timer  = 0.0
        self.started = False
        self.done    = False

    # ------------------------------------------------------------------
    def load_wave(self, entries: list[SpawnEntry]):
        self._queue   = entries[:]
        self._active  = []
        self._timer   = 0.0
        self.started  = False
        self.done     = False

    def start(self):
        self.started = True
        # activate all entries (they use their own delay)
        for entry in self._queue:
            self._active.append({
                "entry":     entry,
                "remaining": entry.count,
                "cd":        entry.delay,
            })

    # ------------------------------------------------------------------
    def update(self, dt: float):
        if not self.started:
            return

        all_done = True
        for stream in self._active:
            if stream["remaining"] <= 0:
                continue
            all_done = False
            stream["cd"] -= dt
            if stream["cd"] <= 0:
                self._spawn(stream["entry"].balloon_id)
                stream["remaining"] -= 1
                stream["cd"] = stream["entry"].interval

        # done when all streams exhausted AND no balloons left
        if all_done and len(self.balloon_group) == 0:
            self.done = True

    def _spawn(self, balloon_id: str):
        balloon = BalloonFactory.spawn(balloon_id, self.path, self.speed_scale)
        self.balloon_group.add(balloon)

    # ------------------------------------------------------------------
    @staticmethod
    def generate_wave(round_num: int) -> list[SpawnEntry]:
        """
        Procedurally build a wave for the given round number.
        Scales difficulty with round progression.
        """
        entries = []

        if round_num <= 5:
            entries.append(SpawnEntry("red",   count=10 + round_num * 4, interval=0.5))
        elif round_num <= 10:
            entries.append(SpawnEntry("red",   count=20, interval=0.4))
            entries.append(SpawnEntry("blue",  count=round_num * 2, interval=0.6, delay=2.0))
        elif round_num <= 20:
            entries.append(SpawnEntry("blue",  count=15, interval=0.35))
            entries.append(SpawnEntry("green", count=10, interval=0.5, delay=3.0))
            if round_num >= 15:
                entries.append(SpawnEntry("yellow", count=5, interval=1.0, delay=5.0))
        elif round_num <= 35:
            entries.append(SpawnEntry("green",  count=12, interval=0.3))
            entries.append(SpawnEntry("yellow", count=8,  interval=0.45))
            entries.append(SpawnEntry("pink",   count=5,  interval=0.8, delay=4.0))
        elif round_num <= 50:
            entries.append(SpawnEntry("pink",   count=15, interval=0.25))
            entries.append(SpawnEntry("black",  count=4,  interval=1.5, delay=5.0))
            entries.append(SpawnEntry("white",  count=4,  interval=1.5, delay=5.0))
        else:
            # late game: MOABs etc.
            entries.append(SpawnEntry("ceramic", count=6,  interval=2.0))
            if round_num >= 60:
                entries.append(SpawnEntry("moab",    count=2,  interval=8.0, delay=10.0))
            if round_num >= 75:
                entries.append(SpawnEntry("bfb",     count=1,  interval=0.0, delay=20.0))

        return entries
