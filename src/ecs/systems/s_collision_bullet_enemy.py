import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

from src.create.prefab_creator import create_explosion

def system_collision_bullet_enemy(world: esper.World, explosion: dict):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagPlayerBullet)
    for bullet_entity, (c_s_b, c_t_b, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s_b.area, c_t_b.pos)
        for enemy_entity, (c_s_e, c_t_e, _) in enemy_components:
            ene_rect = CSurface.get_area_relative(c_s_e.area, c_t_e.pos)
            if bullet_rect.colliderect(ene_rect):
                create_explosion(world, explosion, c_t_e.pos)
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
