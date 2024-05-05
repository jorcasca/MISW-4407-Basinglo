import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_upward import C_Upward

def system_upward_effect(world, upward_velocity: int, screen: pygame.Surface, complete_upward_effect: bool, delta_time: float):
    components = world.get_components(CTransform, C_Upward)
    
    for _, (c_t, c_u) in components:
        if not complete_upward_effect:
            if c_t.pos.y == c_u.final_position.y:
                c_t.pos.y = screen.get_height() + c_t.pos.y
            elif c_t.pos.y > c_u.final_position.y :
                c_t.pos.y -= upward_velocity * delta_time
            else:
                complete_upward_effect = True
        else:
            c_t.pos.y = c_u.final_position.y