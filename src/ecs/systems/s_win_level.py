import esper
import pygame

from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_game_status import CGameStatus, GameStatus
from src.engine.scenes.scene import Scene

def system_win_level(world: esper.World, level: dict, game_status: pygame.Vector2, scene:Scene):
    g_s = world.component_for_entity(game_status, CGameStatus)

    component_count = len(world.get_components(CTagEnemy))
    if component_count == 0:
        level = int(level["settings"]["level"])
        if level < 5:
            scene.switch_scene("LEVEL_0"+str(level+1))
        else: 
            g_s.status = GameStatus.SHOW_GAME_OVER
