"""
MapScene - Roguelite node selection map.
Shows a graph of nodes: Battle, Shop, Elite, Event.
"""

import pygame
import random
from src.ui.scenes.base_scene import BaseScene
from src.core.game import GameState
from src.core.run_state import RunState
from src.core.settings import Settings


NODE_BATTLE = "battle"
NODE_SHOP   = "shop"
NODE_EVENT  = "event"
NODE_ELITE  = "elite"
NODE_BOSS   = "boss"


class MapNode:
    def __init__(self, nid: int, node_type: str, pos: tuple):
        self.nid       = nid
        self.node_type = node_type
        self.pos       = pos
        self.cleared   = False
        self.children: list[int] = []   # node ids

    @property
    def color(self):
        return {
            NODE_BATTLE: (80,  200, 140),
            NODE_SHOP:   (200, 160, 60),
            NODE_EVENT:  (100, 140, 220),
            NODE_ELITE:  (220, 80,  80),
            NODE_BOSS:   (180, 30,  30),
        }.get(self.node_type, (180, 180, 180))

    @property
    def icon(self):
        return {
            NODE_BATTLE: "⚔",
            NODE_SHOP:   "🛒",
            NODE_EVENT:  "?",
            NODE_ELITE:  "💀",
            NODE_BOSS:   "👁",
        }.get(self.node_type, "·")


class MapScene(BaseScene):
    def on_enter(self, run_state: RunState = None, **kwargs):
        if run_state is None:
            run_state = RunState.new_run(self.settings)
        self.run_state = run_state
        self._font     = self.assets.get_font(22)
        self._font_sm  = self.assets.get_font(16)
        self._nodes    = self._generate_map()
        self._current  = 0     # always start at node 0

    # ------------------------------------------------------------------
    def _generate_map(self) -> dict[int, MapNode]:
        s = self.settings
        rng = random
        nodes: dict[int, MapNode] = {}
        cols = 6
        rows = 3
        w, h = s.SCREEN_WIDTH, s.SCREEN_HEIGHT
        margin_x, margin_y = 120, 100
        col_w = (w - 2 * margin_x) // (cols - 1)
        row_h = (h - 2 * margin_y) // (rows - 1)

        nid = 0
        grid: list[list[int]] = []
        for c in range(cols):
            col_nodes = []
            for r in range(rows):
                x = margin_x + c * col_w
                y = margin_y + r * row_h + rng.randint(-20, 20)
                # determine node type
                if c == 0:
                    t = NODE_BATTLE
                elif c == cols - 1:
                    t = NODE_BOSS
                elif rng.random() < s.SHOP_CHANCE:
                    t = NODE_SHOP
                elif rng.random() < s.ELITE_CHANCE:
                    t = NODE_ELITE
                elif rng.random() < s.EVENT_CHANCE:
                    t = NODE_EVENT
                else:
                    t = NODE_BATTLE
                nodes[nid] = MapNode(nid, t, (x, y))
                col_nodes.append(nid)
                nid += 1
            grid.append(col_nodes)

        # connect columns
        for c in range(cols - 1):
            for r in range(rows):
                src = grid[c][r]
                # connect to 1-2 nodes in next column
                targets = rng.sample(grid[c+1], k=min(2, rows))
                for dst in targets:
                    nodes[src].children.append(dst)

        return nodes

    # ------------------------------------------------------------------
    def handle_events(self, events):
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self._try_select_node(ev.pos)

    def _try_select_node(self, pos):
        cur = self._nodes[self._current]
        for nid in cur.children:
            node = self._nodes[nid]
            if pygame.math.Vector2(pos).distance_to(node.pos) < 28:
                self._enter_node(node)

    def _enter_node(self, node: MapNode):
        self._current = node.nid
        if node.node_type in (NODE_BATTLE, NODE_ELITE):
            self.game.change_state(
                GameState.BATTLE,
                run_state=self.run_state,
                node=node,
            )
        elif node.node_type == NODE_SHOP:
            self.game.change_state(GameState.SHOP, run_state=self.run_state)

    # ------------------------------------------------------------------
    def update(self, dt): pass

    def draw(self, surface):
        surface.fill(self.settings.DARK_BG)
        # draw edges
        cur = self._nodes[self._current]
        for nid, node in self._nodes.items():
            for child_id in node.children:
                child = self._nodes[child_id]
                pygame.draw.line(surface, (60, 65, 80), node.pos, child.pos, 2)

        # highlight reachable
        for child_id in cur.children:
            child = self._nodes[child_id]
            pygame.draw.line(surface, self.settings.UI_ACCENT, cur.pos, child.pos, 2)

        # draw nodes
        for nid, node in self._nodes.items():
            reachable = nid in cur.children
            cleared   = node.cleared
            active    = nid == self._current
            r = 24
            color = node.color if (reachable or active) else (60, 65, 80)
            pygame.draw.circle(surface, color, node.pos, r)
            pygame.draw.circle(surface, (255,255,255) if active else color,
                               node.pos, r, 2)
            icon = self._font_sm.render(node.icon, True, (255, 255, 255))
            surface.blit(icon, icon.get_rect(center=node.pos))

        # HUD
        hud = self._font.render(
            f"Gold: {self.run_state.gold}  ❤ {self.run_state.lives}  Round {self.run_state.round_number}",
            True, self.settings.UI_ACCENT
        )
        surface.blit(hud, (20, 20))
