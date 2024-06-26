import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_direction import CDirection, PlayerDirection
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_game_status import CGameStatus, GameStatus

from src.create.prefab_creator import create_explosion

from src.engine.service_locator import ServiceLocator

def system_collision_player_enemy(world: esper.World, player_entity: int, game_status: pygame.Vector2, explosion: dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    pl_d= world.component_for_entity(player_entity, CDirection)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if ene_rect.colliderect(pl_rect) and pl_s.visible:
            create_explosion(world, explosion, c_t.pos)
            world.delete_entity(enemy_entity)
            ServiceLocator.globals_service.reduce_life()
            pl_s.visible = False
            pl_d.direction_x = PlayerDirection.IDLE
            g_s = world.component_for_entity(game_status, CGameStatus)
            g_s.status = GameStatus.PLAYER_RESTART
            g_s.timer = 4
