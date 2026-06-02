"""
Game - Main state machine and loop
States: MAIN_MENU | MAP | BATTLE | SHOP | EVENT | GAME_OVER | VICTORY
"""

import pygame
from src.core.settings import Settings
from src.core.event_bus import EventBus
from src.core.asset_manager import AssetManager


class GameState:
    MAIN_MENU = "main_menu"
    MAP       = "map"        # roguelite node map
    BATTLE    = "battle"     # tower-defense round
    SHOP      = "shop"       # buy/sell/upgrade
    EVENT     = "event"      # random event card
    GAME_OVER = "game_over"
    VICTORY   = "victory"


class Game:
    def __init__(self, screen: pygame.Surface, settings: Settings, clock: pygame.time.Clock):
        self.screen   = screen
        self.settings = settings
        self.clock    = clock

        self.bus    = EventBus()
        self.assets = AssetManager(settings)

        self.state   = GameState.MAIN_MENU
        self.running = True

        # lazy-imported scene objects (avoids circular deps)
        self._scenes: dict = {}
        self._load_scenes()

    # ------------------------------------------------------------------
    # Scene management
    # ------------------------------------------------------------------
    def _load_scenes(self):
        from src.ui.scenes.main_menu_scene import MainMenuScene
        from src.ui.scenes.map_scene       import MapScene
        from src.ui.scenes.battle_scene    import BattleScene
        from src.ui.scenes.shop_scene      import ShopScene

        ctx = {"game": self, "screen": self.screen,
               "settings": self.settings, "bus": self.bus,
               "assets": self.assets}

        self._scenes = {
            GameState.MAIN_MENU: MainMenuScene(ctx),
            GameState.MAP:       MapScene(ctx),
            GameState.BATTLE:    BattleScene(ctx),
            GameState.SHOP:      ShopScene(ctx),
        }

    def change_state(self, new_state: str, **kwargs):
        """Transition to a new scene, passing optional data."""
        self.state = new_state
        scene = self._scenes.get(new_state)
        if scene:
            scene.on_enter(**kwargs)

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        # start at menu
        self.change_state(GameState.MAIN_MENU)

        while self.running:
            dt = self.clock.tick(self.settings.FPS) / 1000.0  # seconds

            # --- events ---
            events = pygame.event.get()
            for ev in events:
                if ev.type == pygame.QUIT:
                    self.running = False
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            # --- update & draw active scene ---
            scene = self._scenes.get(self.state)
            if scene:
                scene.handle_events(events)
                scene.update(dt)
                self.screen.fill(self.settings.DARK_BG)
                scene.draw(self.screen)

            pygame.display.flip()
