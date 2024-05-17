import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

from src.ecs.components.tags.c_tag_shield import CTagShield
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_shield_player(world:esper.World):
    shield_components = world.get_components(CTransform, CSurface, CTagShield)
    player_components = world.get_components(CTransform, CSurface, CTagPlayer)

    for _, (c_t, c_s, _) in player_components:
        for _, (a_c_t, a_c_s, _) in shield_components:
            a_c_s.visible = c_s.visible
            a_c_t.pos.x = c_t.pos.x + c_s.area.size[0]/2 - (a_c_s.area.size[0]/2)
