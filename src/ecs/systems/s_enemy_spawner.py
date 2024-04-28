import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.create.prefab_creator import create_enemy_square

def system_enemy_spawner(world: esper.World, delta_time: float, enemies: dict):
    components = world.get_component(CEnemySpawner)
    for _, c_s in components:
        c_s.spawn_timer += delta_time
        for enemy_spawn in c_s.enemy_spawn_events:
            if not enemy_spawn.get('triggered', False) and c_s.spawn_timer >= enemy_spawn['time']:
                enemy_spawn['triggered'] = True
                enemy_type = enemy_spawn['enemy_type']
                enemy_data = enemies.get(enemy_type)
                if enemy_data:
                    create_enemy_square(ecs_world=world, enemy=enemy_data, enemy_spawn=enemy_spawn)
