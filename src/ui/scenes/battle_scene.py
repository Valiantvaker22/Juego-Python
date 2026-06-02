"""
BattleScene - The tower-defense combat screen.
"""

import pygame
from src.ui.scenes.base_scene import BaseScene
from src.core.game import GameState
from src.core.run_state import RunState
from src.systems.wave_manager import WaveManager
from src.entities.towers.dart_monkey import DartMonkey


class BattleScene(BaseScene):
    # Simple straight path (replace with tilemap data later)
    DEFAULT_PATH = [
        (0, 360), (200, 360), (200, 180), (500, 180),
        (500, 540), (800, 540), (800, 240), (1100, 240),
        (1100, 480), (1280, 480),
    ]

    def on_enter(self, run_state: RunState = None, node=None, **kwargs):
        self.run_state = run_state
        self.node      = node

        self._font     = self.assets.get_font(22)
        self._font_sm  = self.assets.get_font(16)

        # sprite groups
        self.balloon_group    = pygame.sprite.Group()
        self.tower_group      = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()

        # wave
        speed_scale = 1.0 + run_state.round_number * 0.05
        self.wave = WaveManager(self.DEFAULT_PATH, speed_scale, self.balloon_group)
        self.wave.load_wave(WaveManager.generate_wave(run_state.round_number))
        self.wave.start()

        # subscribe to bus
        self.bus.subscribe("balloon_reached_end", self._on_balloon_escaped)

        # selected tower to place
        self._placing_tower = None
        self._tower_class   = DartMonkey

        # state
        self._victory = False
        self._defeat  = False
        self._end_timer = 2.0

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.game.change_state(GameState.MAP, run_state=self.run_state)
                if ev.key == pygame.K_1:
                    self._placing_tower = DartMonkey

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self._placing_tower and not self._victory and not self._defeat:
                    mx, my = ev.pos
                    gx = mx // self.settings.TILE_SIZE
                    gy = my // self.settings.TILE_SIZE
                    cost = self._placing_tower.COST
                    if self.run_state.gold >= cost:
                        tower = self._placing_tower(gx, gy, self.settings.TILE_SIZE)
                        self.tower_group.add(tower)
                        self.run_state.add_gold(-cost)
                    self._placing_tower = None

    # ------------------------------------------------------------------
    def update(self, dt):
        self.wave.update(dt)
        self.balloon_group.update(dt)

        # towers shoot
        for tower in self.tower_group:
            projs = tower.update(dt, self.balloon_group)
            for p in projs:
                self.projectile_group.add(p)

        # projectile movement & collision
        self.projectile_group.update(dt)
        for proj in list(self.projectile_group):
            hits = pygame.sprite.spritecollide(proj, self.balloon_group, False)
            for balloon in hits:
                children = proj.on_hit(balloon)
                for child in children:
                    self.balloon_group.add(child)
                if balloon.alive_flag is False:
                    self.run_state.add_gold(balloon.defn.reward)

        # check end conditions
        if self.wave.done and not self._victory:
            self._victory = True

        if self._victory or self._defeat:
            self._end_timer -= dt
            if self._end_timer <= 0:
                self._finish()

    def _on_balloon_escaped(self, **kwargs):
        lives_lost = kwargs.get("lives", 1)
        game_over = self.run_state.lose_lives(lives_lost)
        if game_over:
            self._defeat = True

    def _finish(self):
        self.bus.unsubscribe("balloon_reached_end", self._on_balloon_escaped)
        if self._victory:
            self.run_state.round_number += 1
            self.run_state.nodes_cleared += 1
            if self.node:
                self.node.cleared = True
            self.run_state.add_gold(self.settings.GOLD_PER_ROUND)
            self.game.change_state(GameState.MAP, run_state=self.run_state)
        else:
            self.game.change_state(GameState.MAIN_MENU)

    # ------------------------------------------------------------------
    def draw(self, surface):
        surface.fill((30, 80, 40))   # green map background
        self._draw_path(surface)

        self.balloon_group.draw(surface)
        self.tower_group.draw(surface)
        self.projectile_group.draw(surface)

        self._draw_hud(surface)

        if self._victory:
            msg = self._font.render("✔ Round Clear!", True, self.settings.UI_ACCENT)
            surface.blit(msg, msg.get_rect(center=(self.settings.SCREEN_WIDTH//2, 80)))
        if self._defeat:
            msg = self._font.render("✘ Game Over", True, self.settings.RED)
            surface.blit(msg, msg.get_rect(center=(self.settings.SCREEN_WIDTH//2, 80)))

        if self._placing_tower:
            mx, my = pygame.mouse.get_pos()
            preview = pygame.Surface((self.settings.TILE_SIZE,)*2, pygame.SRCALPHA)
            preview.fill((100, 220, 140, 80))
            surface.blit(preview, (mx - self.settings.TILE_SIZE//2,
                                    my - self.settings.TILE_SIZE//2))

    def _draw_path(self, surface):
        pts = [pygame.math.Vector2(p) for p in self.DEFAULT_PATH]
        for i in range(len(pts) - 1):
            pygame.draw.line(surface, (180, 150, 80),
                             (int(pts[i].x), int(pts[i].y)),
                             (int(pts[i+1].x), int(pts[i+1].y)), 40)

    def _draw_hud(self, surface):
        panel = pygame.Surface((320, 40), pygame.SRCALPHA)
        panel.fill((20, 22, 30, 180))
        surface.blit(panel, (0, 0))
        text = self._font.render(
            f"Gold: {self.run_state.gold}  ❤ {self.run_state.lives}  Round {self.run_state.round_number}",
            True, self.settings.UI_ACCENT
        )
        surface.blit(text, (10, 8))

        hint = self._font_sm.render("[1] Dart Monkey ($200)  |  ESC: Map", True, (150, 160, 170))
        surface.blit(hint, (10, self.settings.SCREEN_HEIGHT - 28))
