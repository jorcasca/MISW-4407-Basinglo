import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

def system_bullet_bounds(world: esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayerBullet)
    for entity, (c_t, c_s, _) in components:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(cuad_rect):
            world.delete_entity(entity)
