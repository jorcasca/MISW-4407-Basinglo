import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_animation import CAnimation, _set_animation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_state(world: esper.World):
    components = world.get_components(CVelocity, CTransform, CAnimation, CEnemyState, CTagEnemy)

    for _, (c_v, c_t, c_a, c_pst, _) in components:
        _set_animation(c_a, 1)
        if c_pst.state == EnemyState.IDLE_FOWARD:
            _do_idle_foward_state(c_v, c_t, c_pst)
        if c_pst.state == EnemyState.IDLE_BACKWARD:
            _do_idle_backward_state(c_v, c_t, c_pst)
        if c_pst.state == EnemyState.MOVE:
            _do_move_state(c_v, c_pst)

def _do_idle_foward_state(c_v: CVelocity, c_t:CTransform, c_pst: CEnemyState):
    c_v.vel.x = 30
    if c_t.pos.x - c_t.initial_pos.x > 20:
        c_pst.state = EnemyState.IDLE_BACKWARD

def _do_idle_backward_state(c_v: CVelocity, c_t:CTransform, c_pst: CEnemyState):
    c_v.vel.x = -30
    if c_t.pos.x - c_t.initial_pos.x < -20:
        c_pst.state = EnemyState.IDLE_FOWARD

def _do_move_state(c_v: CVelocity, c_pst: CEnemyState):
    pass