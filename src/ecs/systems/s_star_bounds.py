from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar

def system_star_bounds(world, screen):
    components = world.get_components(CTransform, CTagStar)
    for _, (c_t, _) in components:
        if c_t.pos.y > screen.get_height():
            c_t.pos.y = 0
