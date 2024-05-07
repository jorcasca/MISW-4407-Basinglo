

import esper

from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_direction import CDirection

def system_player_state(world:esper.World, player: dict):
    components = world.get_components(CVelocity, CDirection, CTagPlayer)
    for _, (c_v, c_d, _) in components:
        c_v.vel.x = c_d.direction_x.value * player["input_velocity"]
