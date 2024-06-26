import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_shield import CTagShield

from src.create.prefab_creator import create_explosion

def system_collision_shield_enemy(world: esper.World, explosion: dict):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    shield_components = world.get_components(CSurface, CTransform, CTagShield)
    for _, (c_s_b, c_t_b, _) in shield_components:
        bullet_rect = CSurface.get_area_relative(c_s_b.area, c_t_b.pos)
        for enemy_entity, (c_s_e, c_t_e, _) in enemy_components:
            ene_rect = CSurface.get_area_relative(c_s_e.area, c_t_e.pos)
            if bullet_rect.colliderect(ene_rect):
                create_explosion(world, explosion, c_t_e.pos)
                world.delete_entity(enemy_entity)
