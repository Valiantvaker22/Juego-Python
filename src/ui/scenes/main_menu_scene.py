"""
MainMenuScene - Title screen with Play / Quit.
"""

import pygame
from src.ui.scenes.base_scene import BaseScene
from src.core.game import GameState


class MainMenuScene(BaseScene):
    def on_enter(self, **kwargs):
        self._font_title = self.assets.get_font(72, bold=True)
        self._font_btn   = self.assets.get_font(36)
        self._buttons = [
            {"label": "▶  Play",  "action": self._start_run, "rect": pygame.Rect(0,0,260,60)},
            {"label": "✕  Quit",  "action": self._quit,      "rect": pygame.Rect(0,0,260,60)},
        ]
        self._layout_buttons()

    def _layout_buttons(self):
        cx = self.settings.SCREEN_WIDTH // 2
        base_y = self.settings.SCREEN_HEIGHT // 2 + 40
        for i, btn in enumerate(self._buttons):
            btn["rect"].center = (cx, base_y + i * 80)

    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for btn in self._buttons:
                    if btn["rect"].collidepoint(ev.pos):
                        btn["action"]()

    def update(self, dt): pass

    def draw(self, surface):
        surface.fill(self.settings.DARK_BG)

        # Title
        title = self._font_title.render("🎈 Balloon Roguelite", True, self.settings.UI_ACCENT)
        surface.blit(title, title.get_rect(center=(self.settings.SCREEN_WIDTH//2,
                                                    self.settings.SCREEN_HEIGHT//2 - 80)))
        # Buttons
        mx, my = pygame.mouse.get_pos()
        for btn in self._buttons:
            hover = btn["rect"].collidepoint(mx, my)
            color = self.settings.UI_ACCENT if hover else self.settings.WHITE
            pygame.draw.rect(surface, color, btn["rect"], border_radius=8, width=2)
            label = self._font_btn.render(btn["label"], True, color)
            surface.blit(label, label.get_rect(center=btn["rect"].center))

    def _start_run(self):
        self.game.change_state(GameState.MAP)

    def _quit(self):
        self.game.running = False
