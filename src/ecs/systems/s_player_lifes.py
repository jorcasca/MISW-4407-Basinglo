

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_game_status import CGameStatus, GameStatus

from src.engine.service_locator import ServiceLocator

def system_player_lifes(world:esper.World, life1: pygame.Vector2, life2: pygame.Vector2, life3: pygame.Vector2, game_status: pygame.Vector2):
    l1_c_s = world.component_for_entity(life1, CSurface)
    l2_c_s = world.component_for_entity(life2, CSurface)
    l3_c_s = world.component_for_entity(life3, CSurface)
    lifes = ServiceLocator.globals_service.lifes
    if lifes == 2:
        l3_c_s.visible = False
    elif lifes == 1:
        l2_c_s.visible = False
    elif lifes == 0:
        l1_c_s.visible = False
        g_s = world.component_for_entity(game_status, CGameStatus)
        if g_s.status != GameStatus.GAME_OVER:
            g_s.status = GameStatus.SHOW_GAME_OVER
