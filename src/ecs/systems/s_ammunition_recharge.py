import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_player_ammunition import CTagPlayerAmmunition

def system_ammunition_recharge(world: esper.World):
    ammunition_components = world.get_components(CSurface, CTagPlayerAmmunition)
    components = world.get_components(CTransform, CSurface, CTagPlayerBullet)
    for _, (a_c_s, _) in ammunition_components:
        a_c_s.visible = len(components) == 0
