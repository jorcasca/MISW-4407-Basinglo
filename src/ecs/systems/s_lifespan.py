import esper

from src.ecs.components.c_life_span import CLifeSpan

def system_lifespan(ecs_world: esper.World, delta_time: float):
    bullet_fragments_components = ecs_world.get_component(CLifeSpan)
    for entity, (l_s) in bullet_fragments_components:
        l_s.duration -= delta_time
        if l_s.duration <= 0:
            ecs_world.delete_entity(entity)
