import esper
import random

from src.ecs.components.c_enemy_state import CEnemyState, EnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_enemy_spawner import CEnemySpawner

from src.create.prefab_creator import create_enemy_bullet_square

def system_enemy_bullet(world: esper.World, bullet: dict, delta_time: float):
    components = world.get_components(CTransform, CSurface, CEnemyState, CTagEnemy)
    enemy_spawner_component = world.get_component(CEnemySpawner)

    for _, c_s in enemy_spawner_component:
        c_s.spawn_timer += delta_time
        if c_s.spawn_timer >= 3:
            c_s.spawn_timer = 0
            for _, (c_t, c_s, c_pst, _) in components:
                if c_pst.state == EnemyState.CHASE:
                    create_enemy_bullet_square(world, bullet, c_t.pos, c_s.area.size)
            if len(components) > 0:
                _, (c_t, c_s, c_pst, _) = random.choice(components)
                if c_pst.state == EnemyState.IDLE_BACKWARD or c_pst.state == EnemyState.IDLE_FOWARD:
                    create_enemy_bullet_square(world, bullet, c_t.pos, c_s.area.size)
        