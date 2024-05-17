import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

from src.create.prefab_creator import create_explosion

def system_collision_bullet(world: esper.World, explosion: dict):
    bullet_e_components = world.get_components(CTransform, CTagEnemyBullet)
    bullet_p_components = world.get_components(CTransform, CTagPlayerBullet)
    for bullet_e_entity, (c_t_e, _) in bullet_e_components:
        for bullet_p_entity, (c_t_p, _) in bullet_p_components:
            if abs(c_t_e.pos.y - c_t_p.pos.y) < 2 and abs(c_t_e.pos.x - c_t_p.pos.x) < 2:
                new_pos = pygame.Vector2(c_t_p.pos.x - 3, c_t_p.pos.y)
                create_explosion(world, explosion, new_pos)
                world.delete_entity(bullet_e_entity)
                world.delete_entity(bullet_p_entity)
