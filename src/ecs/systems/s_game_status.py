import esper

from src.ecs.components.c_game_status import CGameStatus, GameStatus

from src.create.prefab_creator import create_enemy_spawner

def system_game_status(ecs_world: esper.World, level: dict, delta_time: float):
    bullet_fragments_components = ecs_world.get_component(CGameStatus)
    for _, (g_s) in bullet_fragments_components:
        g_s.timer -= delta_time
        if g_s.timer <= 0:
            if g_s.status == GameStatus.IDLE:
                g_s.status = GameStatus.SHOW_ALIENS
            elif g_s.status == GameStatus.SHOW_ALIENS:
                create_enemy_spawner(ecs_world, level['enemy_spawn_events'], level['settings']['idle_enemy_velocity'])
                g_s.status = GameStatus.START_ALIENS
                g_s.timer = 3                      
            elif g_s.status == GameStatus.START_ALIENS:
                g_s.status = GameStatus.START
