import esper

from src.ecs.components.c_game_status import CGameStatus, GameStatus
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

from src.create.prefab_creator import create_enemy_spawner

from src.engine.service_locator import ServiceLocator

from src.create.prefab_creator import draw_text

def system_game_status(ecs_world: esper.World, level: dict, player_spawn: dict, interface: dict, delta_time: float):
    components = ecs_world.get_component(CGameStatus)
    for _, (g_s) in components:
        g_s.timer -= delta_time
        if g_s.timer <= 0:
            if g_s.status == GameStatus.IDLE:
                g_s.status = GameStatus.SHOW_ALIENS
            elif g_s.status == GameStatus.SHOW_ALIENS:
                create_enemy_spawner(ecs_world, level['enemy_spawn_events'], level['settings']['idle_enemy_velocity'])
                g_s.status = GameStatus.START_ALIENS
                g_s.timer = 1                      
            elif g_s.status == GameStatus.START_ALIENS:
                g_s.status = GameStatus.START
            elif g_s.status == GameStatus.PLAYER_RESTART:
                player_components = ecs_world.get_components(CSurface, CTransform, CTagPlayer)
                for _, (c_s_p, c_t_p, _) in player_components:
                    pl_rect = CSurface.get_area_relative(c_s_p.area, c_t_p.pos)
                    c_t_p.pos.x = player_spawn["position"]["x"] - pl_rect.size[0] / 2
                    c_s_p.visible = True
                g_s.status = GameStatus.START
            elif g_s.status == GameStatus.SHOW_GAME_OVER:
                draw_text(ecs_world, interface["game_over"]["value"], interface["game_over"]["font"], interface["game_over"]["font_size"], interface["game_over"]["color"], interface["game_over"]["position"])
                ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")
                g_s.status = GameStatus.GAME_OVER
                g_s.timer = 3           
