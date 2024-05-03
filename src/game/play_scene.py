import pygame

import src.engine.game_engine

from src.create.prefab_creator import create_player_square, create_input_player, create_player_bullet_square, create_player_ammunition_square, create_enemy_spawner, draw_text, create_sprite, create_starfield

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_blink import CBlink

from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

from src.utils.load_config import load_window, load_enemies, load_player, load_bullet, load_explosion, load_interface, load_starfield

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_bounds import system_player_bounds
from src.ecs.systems.s_bullet_bounds import system_bullet_bounds
from src.ecs.systems.s_ammunition_recharge import system_ammunition_recharge
from src.ecs.systems.s_ammunition_player import system_ammunition_player
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_enemy_bounds import system_enemy_bounds
from src.ecs.systems.s_enemy_bullet import system_enemy_bullet
from src.ecs.systems.s_win_level import system_win_level
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_star_bounds import system_star_bounds

from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, level:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.load_config()
        self.level = level
        self._paused = False
        
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
        create_starfield(self.ecs_world, self.starfield, self.screen)
        draw_text(self.ecs_world, self.interface["1up"]["value"], self.interface["1up"]["font"], self.interface["1up"]["font_size"], self.interface["1up"]["color"], self.interface["1up"]["position"])
        draw_text(self.ecs_world, self.interface["high_score"]["value"], self.interface["high_score"]["font"], self.interface["high_score"]["font_size"], self.interface["high_score"]["color"], self.interface["high_score"]["position"])
        draw_text(self.ecs_world, self.interface["score_value"]["value"], self.interface["score_value"]["font"], self.interface["score_value"]["font_size"], self.interface["score_value"]["color"], self.interface["score_value"]["position"])
        draw_text(self.ecs_world, self.interface["high_score_value"]["value"], self.interface["high_score_value"]["font"], self.interface["high_score_value"]["font_size"], self.interface["high_score_value"]["color"], self.interface["high_score_value"]["position"])
        draw_text(self.ecs_world, self.interface["level_value"]["value"], self.interface["level_value"]["font"], self.interface["level_value"]["font_size"], self.interface["level_value"]["color"], self.interface["level_value"]["position"])
        
        if self.level["settings"]["level"] == 2:
            draw_text(self.ecs_world, self.interface["level_complete"]["value"], self.interface["level_complete"]["font"], self.interface["level_complete"]["font_size"], self.interface["level_complete"]["color"], self.interface["level_complete"]["position"])
        
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["level_img"]["position"]["x"], self.interface["level_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["level_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"], self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+10, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+20, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        self._player_entity = create_player_square(self.ecs_world, self.player, self.level['player_spawn'])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        create_player_ammunition_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)
        create_enemy_spawner(ecs_world=self.ecs_world, enemy_spawn_events=self.level['enemy_spawn_events'])
            
        paused_text_ent = draw_text(self.ecs_world, self.interface["pause"]["value"], self.interface["pause"]["font"], self.interface["pause"]["font_size"], self.interface["pause"]["color"], self.interface["pause"]["position"], CBlink(self.interface["start"]["blink_rate"]))
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused
        self._paused = False

        create_input_player(self.ecs_world)


    def do_update(self, delta_time: float):
        system_blink(self.ecs_world, delta_time)
        system_star_bounds(self.ecs_world, self.screen, delta_time)

        if not self._paused:
            system_movement(self.ecs_world, delta_time)
            system_player_bounds(self.ecs_world, self.screen)
            system_bullet_bounds(self.ecs_world, self.screen)
            system_ammunition_recharge(self.ecs_world)
            system_ammunition_player(self.ecs_world)
            system_enemy_spawner(self.ecs_world, delta_time, self.enemies)
            system_enemy_state(self.ecs_world, self._player_entity, self.enemies, delta_time, self.screen)
            system_collision_bullet_enemy(self.ecs_world, self.explosion['enemy'])
            system_collision_bullet_player(self.ecs_world, self.level['player_spawn'], self.explosion['player'])
            system_collision_player_enemy(self.ecs_world, self._player_entity, self.level['player_spawn'], self.explosion['player'])
            system_explosion_kill(self.ecs_world)
            system_enemy_bounds(self.ecs_world, self.screen)
            system_enemy_bullet(self.ecs_world, self.bullet["enemy"], delta_time)
            system_win_level(self.ecs_world, self)
            system_animation(self.ecs_world, delta_time)
            self.ecs_world._clear_dead_entities()

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if not self._paused:
            if action.name == "PLAYER_LEFT":
                if action.phase == CommandPhase.START:
                    self._player_c_v.vel.x -= self.player["input_velocity"]
                elif action.phase == CommandPhase.END:
                    self._player_c_v.vel.x += self.player["input_velocity"]
            if action.name == "PLAYER_RIGHT":
                if action.phase == CommandPhase.START:
                    self._player_c_v.vel.x += self.player["input_velocity"]
                elif action.phase == CommandPhase.END:
                    self._player_c_v.vel.x -= self.player["input_velocity"]
            if action.name == "PLAYER_FIRE":
                if action.phase == CommandPhase.START:
                    components = self.ecs_world.get_components(CTagPlayerBullet)
                    if len(components) < self.level['player_spawn']['max_bullets']:
                        create_player_bullet_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")

        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused
