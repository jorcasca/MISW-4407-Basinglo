import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

def system_bullet_bounds(world: esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    player_bullet_components = world.get_components(CTransform, CSurface, CTagPlayerBullet)
    enemy_bullet_components = world.get_components(CTransform, CSurface, CTagEnemyBullet)

    for entity, (c_t, c_s, _) in player_bullet_components:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(cuad_rect):
            world.delete_entity(entity)
            
    for entity, (c_t, c_s, _) in enemy_bullet_components:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if not screen_rect.contains(cuad_rect):
            world.delete_entity(entity)
