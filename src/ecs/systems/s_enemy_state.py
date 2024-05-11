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
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def system_enemy_state(world: esper.World, player_entity: pygame.Vector2, enemy_spawn: dict, delta_time: float, screen:pygame.Surface):
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    components = world.get_components(CSurface, CVelocity, CTransform, CAnimation, CEnemyState, CTagEnemy)

    chase_detected = False

    for _, (c_s, c_v, c_t, c_a, c_pst, c_t_e) in components:
        _set_animation(c_a, 1)
        if c_pst.state == EnemyState.IDLE:
            _do_idle_state()
        if c_pst.state == EnemyState.ROTATE:
            chase_detected = True
            _do_rotate_state(c_a, c_s, c_t, c_pst, pl_t, pl_s, enemy_spawn[c_t_e.type]["velocity"], enemy_spawn[c_t_e.type]["image"], enemy_spawn[c_t_e.type]["image_pivote"], delta_time)
        if c_pst.state == EnemyState.CHASE:
            chase_detected = True
            _do_chase_state(c_a, c_s, c_t, c_pst, pl_t, pl_s, enemy_spawn[c_t_e.type]["velocity"], enemy_spawn[c_t_e.type]["image"], enemy_spawn[c_t_e.type]["image_pivote"], delta_time)
        if c_pst.state == EnemyState.RETURN:
            _do_return_state(world, c_a, c_s, c_t, c_pst, enemy_spawn[c_t_e.type]["velocity"], screen, enemy_spawn[c_t_e.type]["image"], enemy_spawn[c_t_e.type]["image_pivote"], delta_time)

    if len(components) > 0 and pl_s.visible and not chase_detected:
        _, (_, c_v2, _, _, c_pst2, c_t_e2) = random.choice(components)

        ServiceLocator.sounds_service.play(enemy_spawn[c_t_e2.type]["sound"])
        c_pst2.state = EnemyState.ROTATE

        if (random.random()*(len(enemy_spawn) / len(components))) > 0.1 and len(components) > 1: 
            _, (_, c_v3, _, _, c_pst3, c_t_e3) = random.choice(components)
            c_pst3.state = EnemyState.ROTATE


def _do_idle_state():
    pass

def _do_rotate_state(c_a: CAnimation, c_s: CSurface, c_t: CTransform, c_pst: CEnemyState, pl_t: CTransform, pl_s: CSurface, velocity: int, spride: str, image_pivote: str, delta_time: float):
    direction = pygame.Vector2(pl_t.pos.x + pl_s.area.size[0]/2, - pl_t.pos.y) - c_t.pos
    _move_towards_target(c_t, direction, velocity, delta_time) 
    if c_s.angle > -180: 
        c_a.enabled = False
        c_s.rotate(ServiceLocator.images_service.get(image_pivote), -4)

    if c_t.pos.y - c_t.initial_pos.y <= -20:
        c_pst.state = EnemyState.CHASE

def _do_chase_state(c_a: CAnimation, c_s: CSurface, c_t: CTransform, c_pst: CEnemyState, pl_t: CTransform, pl_s: CSurface, velocity: int, spride: str, image_pivote: str, delta_time: float):
    correct_pl_pos = pygame.Vector2(pl_t.pos.x + pl_s.area.size[0]/2, pl_t.pos.y)
    if correct_pl_pos.y - c_t.pos.y < 5:
        c_pst.state = EnemyState.RETURN 
    else:
        if c_s.angle > -180 and c_a.enabled == False: 
            c_s.rotate(ServiceLocator.images_service.get(image_pivote), -4)
        elif c_s.angle < 180:
                c_s.rotate_to_180(ServiceLocator.images_service.get(spride))
                c_a.enabled = True
        direction = correct_pl_pos - c_t.pos
        _move_towards_target(c_t, direction, velocity, delta_time)


def _do_return_state(world, c_a: CAnimation, c_s: CSurface, c_t: CTransform, c_pst: CEnemyState, velocity: int, screen:pygame.Surface, spride: str, image_pivote: str, delta_time: float):
    for _, c_e_s in world.get_component(CEnemySpawner):
        direction = c_t.initial_pos - c_t.pos
        direction.x = direction.x + c_e_s.idle_base_position
        if direction.magnitude_squared() > 1:
                if screen.get_height() - c_t.pos.y < 50:
                    direction.y = screen.get_height() - c_t.pos.y
                    _move_towards_target(c_t, direction, velocity, delta_time) 
                else:   
                    if c_s.angle > 0 and c_t.pos.y - c_t.initial_pos.y >= -40: 
                        c_a.enabled = False
                        c_s.rotate(ServiceLocator.images_service.get(image_pivote), 4)
                    _move_towards_target(c_t, direction, velocity, delta_time)
        else:
            c_s.surf = ServiceLocator.images_service.get(spride)
            c_a.enabled = True
            c_pst.state = EnemyState.IDLE 


def _move_towards_target(c_t: CTransform, direction: pygame.Vector2, velocity: float, delta_time: float):
        direction.normalize_ip()
        c_t.pos += direction * velocity * delta_time
