"""
ShopScene - Buy towers, relics, and upgrades between battles.
"""

import pygame
from src.ui.scenes.base_scene import BaseScene
from src.core.game import GameState
from src.core.run_state import RunState


class ShopScene(BaseScene):
    def on_enter(self, run_state: RunState = None, **kwargs):
        self.run_state = run_state
        self._font     = self.assets.get_font(28)
        self._font_sm  = self.assets.get_font(20)

    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.game.change_state(GameState.MAP, run_state=self.run_state)

    def update(self, dt): pass

    def draw(self, surface):
        surface.fill(self.settings.UI_PANEL)
        title = self._font.render("🛒  Shop  —  [ESC] to leave", True, self.settings.UI_ACCENT)
        surface.blit(title, (40, 40))
        info = self._font_sm.render(
            f"Gold: {self.run_state.gold}", True, self.settings.WHITE
        )
        surface.blit(info, (40, 90))
        # TODO: shop items grid
        placeholder = self._font_sm.render("Shop items coming soon...", True, (120, 130, 140))
        surface.blit(placeholder, (40, 160))
