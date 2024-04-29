import asyncio
import pygame
import esper

from src.create.prefab_creator import create_player_square, create_input_player, create_player_bullet_square, create_player_ammunition_square, create_enemy_spawner, draw_text, create_sprite

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet

from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_player_bounds import system_player_bounds
from src.ecs.systems.s_player_input import system_player_input
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
from src.engine.service_locator import ServiceLocator

from src.utils.load_config import load_window, load_level_01, load_enemies, load_player, load_bullet, load_explosion, load_interface

class GameEngine:
    def __init__(self) -> None:
        self.load_config()
        self.setup_game()

    def load_config(self):
        self.window = load_window()
        self.level = load_level_01()
        self.enemies = load_enemies()
        self.player = load_player()
        self.bullet = load_bullet()
        self.explosion = load_explosion()
        self.interface = load_interface()

    def setup_game(self):
        pygame.init()
        window_size = self.window['size']
        self.screen = pygame.display.set_mode((window_size['w'], window_size['h']), 0)
        pygame.display.set_caption(self.window['title'])
        self.max_bullets = self.level['player_spawn']['max_bullets']
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.is_paused = False
        self.delta_time = 0
        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        draw_text(self.ecs_world, self.interface["1up"]["value"], self.interface["1up"]["font"], self.interface["1up"]["font_size"], self.interface["1up"]["color"], self.interface["1up"]["position"])
        draw_text(self.ecs_world, self.interface["high_score"]["value"], self.interface["high_score"]["font"], self.interface["high_score"]["font_size"], self.interface["high_score"]["color"], self.interface["high_score"]["position"])
        draw_text(self.ecs_world, self.interface["score_value"]["value"], self.interface["score_value"]["font"], self.interface["score_value"]["font_size"], self.interface["score_value"]["color"], self.interface["score_value"]["position"])
        draw_text(self.ecs_world, self.interface["high_score_value"]["value"], self.interface["high_score_value"]["font"], self.interface["high_score_value"]["font_size"], self.interface["high_score_value"]["color"], self.interface["high_score_value"]["position"])
        draw_text(self.ecs_world, self.interface["level_value"]["value"], self.interface["level_value"]["font"], self.interface["level_value"]["font_size"], self.interface["level_value"]["color"], self.interface["level_value"]["position"])
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["level_img"]["position"]["x"], self.interface["level_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["level_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"], self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+10, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["life_img"]["position"]["x"]+20, self.interface["life_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["life_img"]["image"]))

        create_input_player(self.ecs_world)
        self._player_entity = create_player_square(self.ecs_world, self.player, self.level['player_spawn'])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_c_t = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_c_s = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        create_player_ammunition_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)
        create_enemy_spawner(ecs_world=self.ecs_world, enemy_spawn_events=self.level['enemy_spawn_events'])

    def _calculate_time(self):
        self.clock.tick(self.window['framerate'])
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            system_player_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _do_action(self, c_input: CInputCommand):
        if not self.is_paused:
            if c_input.name == "PLAYER_LEFT":
                if c_input.phase == CommandPhase.START:
                    self._player_c_v.vel.x -= self.player["input_velocity"]
                elif c_input.phase == CommandPhase.END:
                    self._player_c_v.vel.x += self.player["input_velocity"]
            if c_input.name == "PLAYER_RIGHT":
                if c_input.phase == CommandPhase.START:
                    self._player_c_v.vel.x += self.player["input_velocity"]
                elif c_input.phase == CommandPhase.END:
                    self._player_c_v.vel.x -= self.player["input_velocity"]
            if c_input.name == "PLAYER_FIRE":
                if c_input.phase == CommandPhase.START:
                    components = self.ecs_world.get_components(CTagPlayerBullet)
                    if len(components) < self.level['player_spawn']['max_bullets']:
                        create_player_bullet_square(self.ecs_world, self.bullet["player"], self._player_c_t.pos, self._player_c_s.area.size)

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_player_bounds(self.ecs_world, self.screen)
        system_bullet_bounds(self.ecs_world, self.screen)
        system_ammunition_recharge(self.ecs_world)
        system_ammunition_player(self.ecs_world)
        system_enemy_spawner(self.ecs_world, self.delta_time, self.enemies)
        system_enemy_state(self.ecs_world, self._player_entity, self.enemies, self.delta_time, self.screen)
        system_collision_bullet_enemy(self.ecs_world, self.explosion['enemy'])
        system_collision_bullet_player(self.ecs_world, self.level['player_spawn'], self.explosion['player'])
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level['player_spawn'], self.explosion['player'])
        system_explosion_kill(self.ecs_world)
        system_enemy_bounds(self.ecs_world, self.screen)
        system_enemy_bullet(self.ecs_world, self.bullet["enemy"], self.delta_time)
        system_animation(self.ecs_world, self.delta_time)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        bg_color = self.window['bg_color']
        self.screen.fill((bg_color['r'], bg_color['g'], bg_color['b']))
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
