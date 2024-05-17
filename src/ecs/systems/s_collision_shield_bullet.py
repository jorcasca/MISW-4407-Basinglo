import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_shield import CTagShield
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

from src.create.prefab_creator import create_explosion

def system_collision_shield_bullet(world: esper.World, explosion: dict):
    shield_components = world.get_components(CSurface, CTransform, CTagShield)
    bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for bullet_entity, (c_s_b, c_t_b, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s_b.area, c_t_b.pos)
        for _, (c_s_p, c_t_p, _) in shield_components:
            pl_rect = CSurface.get_area_relative(c_s_p.area, c_t_p.pos)
            if bullet_rect.colliderect(pl_rect):
                create_explosion(world, explosion, c_t_b.pos)
                world.delete_entity(bullet_entity)
