from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar

def system_star_bounds(world, screen, delta_time):
    components = world.get_components(CTransform, CVelocity, CTagStar)
    for _, (c_t, c_v, _) in components:
        c_t.pos.y += c_v.vel.y * delta_time
        if c_t.pos.y > screen.get_height():
            c_t.pos.y = 0
