import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_direction import CDirection, PlayerDirection
from src.ecs.components.c_lifes import CLifes
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.c_game_status import CGameStatus, GameStatus

from src.create.prefab_creator import create_explosion

def system_collision_bullet_player(world: esper.World, explosion: dict, game_status: pygame.Vector2):
    player_components = world.get_components(CSurface, CTransform, CLifes, CDirection, CTagPlayer)
    bullet_components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for bullet_entity, (c_s_b, c_t_b, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(c_s_b.area, c_t_b.pos)
        for _, (c_s_p, c_t_p, c_l_p, c_d_p, _) in player_components:
            pl_rect = CSurface.get_area_relative(c_s_p.area, c_t_p.pos)
            if bullet_rect.colliderect(pl_rect) and c_s_p.visible:
                create_explosion(world, explosion, c_t_b.pos)
                world.delete_entity(bullet_entity)
                c_l_p.lifes -= 1
                c_s_p.visible = False
                c_d_p.direction_x = PlayerDirection.IDLE
                g_s = world.component_for_entity(game_status, CGameStatus)
                g_s.status = GameStatus.PLAYER_RESTART
                g_s.timer = 3
