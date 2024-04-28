import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation, _set_animation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CEnemyState, CTagEnemy)
    for _, (c_v, c_a, c_pst, _) in components:
        _set_animation(c_a, 1)

        if c_pst.state == EnemyState.IDLE:
            _do_idle_state(c_v, c_pst)
        if c_pst.state == EnemyState.MOVE:
            _do_move_state(c_v, c_pst)

def _do_idle_state(c_v: CVelocity, c_pst: CEnemyState):
    if c_v.vel.magnitude_squared() > 0:
        c_pst.state = EnemyState.MOVE

def _do_move_state(c_v: CVelocity, c_pst: CEnemyState):
    if c_v.vel.magnitude_squared() <= 0:
        c_pst.state = EnemyState.IDLE
