"""
RunState - Data that persists across the entire roguelite run.
Passed between scenes via Game.change_state().
"""

from dataclasses import dataclass, field
from src.core.settings import Settings


@dataclass
class TowerSlot:
    tower_id:  str
    upgrades:  list[str] = field(default_factory=list)
    quantity:  int = 1


@dataclass
class RunState:
    # economy
    gold:  int = 0
    lives: int = 0

    # progress
    current_node:   int = 0
    round_number:   int = 1
    nodes_cleared:  int = 0

    # collection
    towers:  list[TowerSlot] = field(default_factory=list)
    relics:  list[str]       = field(default_factory=list)   # passive items
    perks:   list[str]       = field(default_factory=list)   # active abilities

    # flags
    is_elite_round: bool = False

    @classmethod
    def new_run(cls, settings: Settings) -> "RunState":
        return cls(gold=settings.STARTING_GOLD, lives=settings.STARTING_LIVES)

    def add_gold(self, amount: int):
        self.gold = max(0, self.gold + amount)

    def lose_lives(self, amount: int) -> bool:
        """Returns True if game over."""
        self.lives = max(0, self.lives - amount)
        return self.lives <= 0
