import esper
import pygame
import random

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_animation import CAnimation, _set_animation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def system_enemy_state(world: esper.World, player_entity: pygame.Vector2, enemy_spawn: dict, delta_time: float, screen:pygame.Surface):
    pl_t = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CSurface, CVelocity, CTransform, CAnimation, CEnemyState, CTagEnemy)
    chase_detected = False

    current_state = EnemyState.IDLE_FOWARD
    for _, (c_s, c_v, c_t, c_a, c_pst, c_t_e) in components:
        _set_animation(c_a, 1)
        if c_pst.state == EnemyState.IDLE_FOWARD:
            current_state = EnemyState.IDLE_FOWARD
            _do_idle_foward_state(c_v, c_t, c_pst)
        if c_pst.state == EnemyState.IDLE_BACKWARD:
            current_state = EnemyState.IDLE_BACKWARD
            _do_idle_backward_state(c_v, c_t, c_pst)
        if c_pst.state == EnemyState.CHASE:
            chase_detected = True
            _do_chase_state(c_s, c_t, c_pst, pl_t, enemy_spawn[c_t_e.type]["velocity"], delta_time)
        if c_pst.state == EnemyState.RETURN:
            _do_return_state(c_s, c_t, c_pst, enemy_spawn[c_t_e.type]["velocity"], delta_time, screen, current_state)

    if len(components) > 0 and not chase_detected:
        _, (_, c_v2, _, _, c_pst2, c_t_e2) = random.choice(components)
        ServiceLocator.sounds_service.play(enemy_spawn[c_t_e2.type]["sound"])
        c_v2.vel.x = 0
        c_pst2.state = EnemyState.CHASE


def _do_idle_foward_state(c_v: CVelocity, c_t:CTransform, c_pst: CEnemyState):
    c_v.vel.x = 30
    if c_t.pos.x - c_t.initial_pos.x > 20:
        c_pst.state = EnemyState.IDLE_BACKWARD

def _do_idle_backward_state(c_v: CVelocity, c_t:CTransform, c_pst: CEnemyState):
    c_v.vel.x = -30
    if c_t.pos.x - c_t.initial_pos.x < -20:
        c_pst.state = EnemyState.IDLE_FOWARD


def _do_chase_state(c_s: CSurface, c_t: CTransform, c_pst: CEnemyState, pl_t: CTransform, velocity: int, delta_time: float):
    if pl_t.pos.y - c_t.pos.y < 5:
        c_pst.state = EnemyState.RETURN 
    else:
        if c_s.angle < 180: 
            c_s.rotate(180)
        direction = pl_t.pos - c_t.pos
        _move_towards_target(c_t, direction, velocity, delta_time)


def _do_return_state(c_s: CSurface, c_t: CTransform, c_pst: CEnemyState, velocity: int, delta_time: float, screen:pygame.Surface, stateIfReturn: EnemyState):
    direction = c_t.initial_pos - c_t.pos
    if direction.magnitude_squared() > 0.5:
            if screen.get_height() - c_t.pos.y < 50:
                direction.y = screen.get_height() - c_t.pos.y
                _move_towards_target(c_t, direction, velocity, delta_time) 
            else:   
                if c_s.angle > 0: 
                    c_s.rotate(180)
                _move_towards_target(c_t, direction, velocity, delta_time)
    else:
        c_pst.state = stateIfReturn


def _move_towards_target(c_t: CTransform, direction: pygame.Vector2, velocity: float, delta_time: float):
        direction.normalize_ip()
        c_t.pos += direction * velocity * delta_time
