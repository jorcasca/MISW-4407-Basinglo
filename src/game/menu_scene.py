import pygame

import src.engine.game_engine

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand 
from src.ecs.components.c_blink import CBlink

from src.create.prefab_creator import draw_text, create_sprite, create_starfield
from src.utils.load_config import load_interface, load_starfield
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_star_bounds import system_star_bounds
from src.engine.service_locator import ServiceLocator

class MenuScene(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.load_config()

    def load_config(self):
        self.interface = load_interface()
        self.starfield = load_starfield()

    def do_create(self):
        create_starfield(self.ecs_world, self.starfield, self.screen)
        draw_text(self.ecs_world, self.interface["1up"]["value"], self.interface["1up"]["font"], self.interface["1up"]["font_size"], self.interface["1up"]["color"], self.interface["1up"]["position"])
        draw_text(self.ecs_world, self.interface["high_score"]["value"], self.interface["high_score"]["font"], self.interface["high_score"]["font_size"], self.interface["high_score"]["color"], self.interface["high_score"]["position"])
        draw_text(self.ecs_world, self.interface["score_value"]["value"], self.interface["score_value"]["font"], self.interface["score_value"]["font_size"], self.interface["score_value"]["color"], self.interface["score_value"]["position"])
        draw_text(self.ecs_world, self.interface["high_score_value"]["value"], self.interface["high_score_value"]["font"], self.interface["high_score_value"]["font_size"], self.interface["high_score_value"]["color"], self.interface["high_score_value"]["position"])
        draw_text(self.ecs_world, self.interface["start"]["value"], self.interface["start"]["font"], self.interface["start"]["font_size"], self.interface["start"]["color"], self.interface["start"]["position"], CBlink(self.interface["start"]["blink_rate"]))
        create_sprite(self.ecs_world, pygame.Vector2(self.interface["logo_title_img"]["position"]["x"], self.interface["logo_title_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["logo_title_img"]["image"]))
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action, CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time: float):
        system_blink(self.ecs_world, delta_time)
        system_star_bounds(self.ecs_world, self.screen, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")
