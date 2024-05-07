import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_lifes import CLifes
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

from src.create.prefab_creator import create_explosion

def system_collision_bullet_player(world: esper.World, player_spawn: dict, explosion: dict):
    player_components = world.get_components(CSurface, CTransform, CLifes, CTagPlayer)
    bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for bullet_entity, (c_s_b, c_t_b, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s_b.area, c_t_b.pos)
        for _, (c_s_p, c_t_p, c_l_p, _) in player_components:
            pl_rect = CSurface.get_area_relative(c_s_p.area, c_t_p.pos)
            if bullet_rect.colliderect(pl_rect):
                create_explosion(world, explosion, c_t_b.pos)
                world.delete_entity(bullet_entity)
                c_t_p.pos.x = player_spawn["position"]["x"] - pl_rect.size[0] / 2
                c_l_p.lifes -= 1
