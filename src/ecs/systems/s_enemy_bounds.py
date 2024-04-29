import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_bounds(world: esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    for _, (c_t, c_v, c_s, t_e) in components:
        screen_rect = screen.get_rect()
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            c_t.pos.x = cuad_rect.x
        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_t.pos.y = 0
