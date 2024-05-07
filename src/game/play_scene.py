import pygame

import src.engine.game_engine

from src.create.prefab_creator import create_player_square, create_input_player, create_player_bullet_square, create_player_ammunition_square, draw_text, create_sprite, create_starfield, create_game_status

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_life_span import CLifeSpan
from src.ecs.components.c_lifes import CLifes
from src.ecs.components.c_direction import CDirection, PlayerDirection
from src.ecs.components.c_game_status import CGameStatus, GameStatus

from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_score import CTagScore

from src.utils.load_config import load_window, load_enemies, load_player, load_bullet, load_explosion, load_interface, load_starfield

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bounds import system_player_bounds
from src.ecs.systems.s_bullet_bounds import system_bullet_bounds
from src.ecs.systems.s_ammunition_recharge import system_ammunition_recharge
from src.ecs.systems.s_ammunition_player import system_ammunition_player
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_enemy_idle import system_enemy_idle
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_enemy_bounds import system_enemy_bounds
from src.ecs.systems.s_enemy_bullet import system_enemy_bullet
from src.ecs.systems.s_win_level import system_win_level
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_star_bounds import system_star_bounds
from src.ecs.systems.s_lifespan import system_lifespan
from src.ecs.systems.s_player_lifes import system_player_lifes
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_game_status import system_game_status
from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, level:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.load_config()
        self.level = level

    def load_config(self):
        self.window = load_window()
        self.enemies = load_enemies()
        self.player = load_player()
        self.bullet = load_bullet()
        self.explosion = load_explosion()
        self.interface = load_interface()
        self.starfield = load_starfield()

    def do_create(self):
        ServiceLocator.sounds_service.play(self.level["settings"]["sound"])
        self._game_entity = create_game_status(self.ecs_world)
        self._game_c_s = self.ecs_world.component_for_entity(self._game_entity, CGameStatus)

        create_starfield(self.ecs_world, self.starfield, self.screen)
        draw_text(self.ecs_world, self.interface["1up"]["value"], self.interface["1up"]["font"], self.interface["1up"]["font_size"], self.interface["1up"]["color"], self.interface["1up"]["position"])
        draw_text(self.ecs_world, self.interface["high_score"]["value"], self.interface["high_score"]["font"], self.interface["high_score"]["font_size"], self.interface["high_score"]["color"], self.interface["high_score"]["position"])
        draw_text(self.ecs_world, str(ServiceLocator.globals_service.score), self.interface["score_value"]["font"], self.interface["score_value"]["font_size"], self.interface["score_value"]["color"], self.interface["score_value"]["position"], CTagScore())
        draw_text(self.ecs_world, self.interface["high_score_value"]["value"], self.interface["high_score_value"]["font"], self.interface["high_score_value"]["font_size"], self.interface["high_score_value"]["color"], self.interface["high_score_value"]["position"])
        draw_text(self.ecs_world, self.level["settings"]["level"], self.interface["level_value"]["font"], self.interface["level_value"]["font_size"], self.interface["level_value"]["color"], self.interface["level_value"]["position"])
        
        if self.level["settings"]["level"] == "01":
            draw_text(self.ecs_world, self.interface["game_start"]["value"], self.interface["game_start"]["font"], self.interface["game_start"]["font_size"], self.interface["game_start"]["color"], self.interface["game_start"]["position"], CLifeSpan(self.interface["game_start"]["lifespan"]))
        elif self.level["settings"]["level"] == "02":
            draw_text(self.ecs_world, self.interface["level_complete"]["value"], self.interface["level_complete"]["font"], self.interface["level_complete"]["font_size"], self.interface["level_complete"]["color"], self.interface["level_complete"]["position"], CLifeSpan(self.interface["level_complete"]["lifespan"]))
            draw_text(self.ecs_world, self.interface["next_level"]["value"], self.interface["next_level"]["font"], self.interface["next_level"]["font_size"], self.interface["next_level"]["color"], self.interface["next_level"]["position"], CLifeSpan(self.interface["next_level"]["lifespan"]))

        create_sprite(self.ecs_world, pygame.Vector2(self.interface["level_img"]["position"]["x"], self.interface["level_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["level_img"]["image"]))
        self._lf1_entity = create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"], self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        self._lf2_entity = create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+10, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        self._lf3_entity = create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+20, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        self._player_entity = create_player_square(self.ecs_world, self.player, self.level['player_spawn'])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_c_l = self.ecs_world.component_for_entity(self._player_entity, CLifes)
        self._player_c_d = self.ecs_world.component_for_entity(self._player_entity, CDirection)

        create_player_ammunition_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)
            
        paused_text_ent = draw_text(self.ecs_world, self.interface["pause"]["value"], self.interface["pause"]["font"], self.interface["pause"]["font_size"], self.interface["pause"]["color"], self.interface["pause"]["position"], CBlink(self.interface["start"]["blink_rate"]))
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = False

        create_input_player(self.ecs_world)


    def do_update(self, delta_time: float):
        system_blink(self.ecs_world, delta_time)
        system_star_bounds(self.ecs_world, self.screen, delta_time)

        if self._player_c_l.lifes == 0:
           self._game_c_s.status = GameStatus.GAME_OVER

        if self._game_c_s.status != GameStatus.PAUSE and self._game_c_s.status != GameStatus.GAME_OVER:
            system_game_status(self.ecs_world, self.level, delta_time)
            system_movement(self.ecs_world, delta_time)
            system_player_state(self.ecs_world, self.player)
            system_player_bounds(self.ecs_world, self.screen)
            system_bullet_bounds(self.ecs_world, self.screen)
            system_ammunition_recharge(self.ecs_world)
            system_ammunition_player(self.ecs_world)
            system_enemy_spawner(self.ecs_world, delta_time, self.enemies)
            
            if self._game_c_s.status == GameStatus.START:
                system_win_level(self.ecs_world, self)
                system_enemy_state(self.ecs_world, self._player_entity, self.enemies, delta_time, self.screen)
                
            system_enemy_idle(self.ecs_world, self.screen)
            system_collision_bullet_enemy(self.ecs_world, self.interface, self.explosion['enemy'])
            system_collision_bullet_player(self.ecs_world, self.level['player_spawn'], self.explosion['player'])
            system_collision_player_enemy(self.ecs_world, self._player_entity, self.level['player_spawn'], self.explosion['player'])
            system_explosion_kill(self.ecs_world)
            system_enemy_bounds(self.ecs_world, self.screen)
            system_enemy_bullet(self.ecs_world, self.bullet["enemy"], delta_time)
            system_lifespan(self.ecs_world, delta_time)
            system_player_lifes(self.ecs_world, self._lf1_entity, self._lf2_entity, self._lf3_entity, self.interface)
            system_animation(self.ecs_world, delta_time)
            self.ecs_world._clear_dead_entities()

    def do_clean(self):
        self._game_c_s.status = GameStatus.IDLE

    def do_action(self, action: CInputCommand):
        if self._game_c_s.status != GameStatus.PAUSE:
            if action.name == "PLAYER_LEFT":
                if action.phase == CommandPhase.START:
                    self._player_c_d.direction_x = PlayerDirection.LEFT if self._player_c_d.direction_x != PlayerDirection.RIGHT else PlayerDirection.IDLE
                elif action.phase == CommandPhase.END:
                    self._player_c_d.direction_x = PlayerDirection.RIGHT if self._player_c_d.direction_x == PlayerDirection.IDLE else PlayerDirection.IDLE
            elif action.name == "PLAYER_RIGHT":
                if action.phase == CommandPhase.START:
                    self._player_c_d.direction_x =  PlayerDirection.RIGHT if self._player_c_d.direction_x != PlayerDirection.LEFT else PlayerDirection.IDLE
                elif action.phase == CommandPhase.END:
                    self._player_c_d.direction_x = PlayerDirection.LEFT if self._player_c_d.direction_x == PlayerDirection.IDLE else PlayerDirection.IDLE
            if action.name == "PLAYER_FIRE" and self._game_c_s.status == GameStatus.START:
                if action.phase == CommandPhase.START:
                    components = self.ecs_world.get_components(CTagPlayerBullet)
                    if len(components) < self.level['player_spawn']['max_bullets']:
                        create_player_bullet_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START and self._game_over:
            self.switch_scene("MENU_SCENE")

        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            if(self._game_c_s.status == GameStatus.PAUSE):
                self._game_c_s.status = GameStatus.START
            else:
                self._game_c_s.status = GameStatus.PAUSE
            self.p_txt_s.visible = self._game_c_s.status == GameStatus.PAUSE
            if self._game_c_s.status == GameStatus.PAUSE:
                ServiceLocator.sounds_service.play("assets/snd/game_paused.ogg")
