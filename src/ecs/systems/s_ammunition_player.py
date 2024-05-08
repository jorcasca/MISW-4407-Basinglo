import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_ammunition import CTagPlayerAmmunition
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_ammunition_player(world:esper.World):
    ammunition_components = world.get_components(CTransform, CSurface, CTagPlayerAmmunition)
    player_components = world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (c_t, c_s, _) in player_components:
            for _, (a_c_t, a_c_s, _) in ammunition_components:
                a_c_s.visible = c_s.visible
                a_c_t.pos.x = c_t.pos.x + c_s.area.size[0]/2 - (a_c_s.area.size[0]/2)
