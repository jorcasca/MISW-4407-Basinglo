

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_lifes import CLifes
from src.ecs.components.tags.c_tag_player import CTagPlayer

from src.engine.service_locator import ServiceLocator

from src.create.prefab_creator import draw_text

def system_player_lifes(world:esper.World, life1: pygame.Vector2, life2: pygame.Vector2, life3: pygame.Vector2, interface: dict):
    components = world.get_components(CLifes, CTagPlayer)
    for _, (c_l, _) in components:
        l1_c_s = world.component_for_entity(life1, CSurface)
        l2_c_s = world.component_for_entity(life2, CSurface)
        l3_c_s = world.component_for_entity(life3, CSurface)

        if c_l.lifes == 2:
            l3_c_s.visible = False
        elif c_l.lifes == 1:
            l2_c_s.visible = False
        elif c_l.lifes == 0:
            l1_c_s.visible = False
            draw_text(world, interface["game_over"]["value"], interface["game_over"]["font"], interface["game_over"]["font_size"], interface["game_over"]["color"], interface["game_over"]["position"])
            ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")
