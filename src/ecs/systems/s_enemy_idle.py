import esper
import pygame

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_idle(world: esper.World, screen:pygame.Surface):
    screen_width = screen.get_width()
    start_e = screen_width
    end_e = 0
    horizontal_padding = 0.1
    left_wall = screen_width * horizontal_padding
    right_wall = screen_width * (1-horizontal_padding)

    enemy_components = world.get_components(CTransform, CVelocity, CSurface, CEnemyState, CTagEnemy)

    for _, c_e_s in world.get_component(CEnemySpawner):
        first = False
        for _, (c_t, c_v, c_s, c_pst, _) in enemy_components:
            if c_pst.state == EnemyState.IDLE:
                start_e = min(start_e, c_t.pos.x + c_s.area.size[0]/2)
                end_e = max(end_e, c_t.pos.x + c_s.area.size[0]/2)
                if first == False:
                    c_e_s.idle_base_position = c_t.pos.x - c_t.initial_pos.x
                    first = True

        if start_e < left_wall or end_e > right_wall:
            c_e_s.idle_enemy_velocity *= -1

            for _, (c_t, c_v, c_s, c_pst, _) in enemy_components:
                if c_pst.state == EnemyState.IDLE:
                    c_v.vel.x = c_e_s.idle_enemy_velocity

        for _, (c_t, c_v, c_s, c_pst, _) in enemy_components:
            if c_pst.state == EnemyState.IDLE and c_v.vel.x == 0:
                c_v.vel.x = c_e_s.idle_enemy_velocity
