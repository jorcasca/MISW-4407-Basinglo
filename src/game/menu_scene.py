import pygame

import src.engine.game_engine

from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_upward import C_Upward

from src.create.prefab_creator import draw_text, create_sprite, create_starfield, create_menu_input
from src.utils.load_config import load_interface, load_starfield, load_window
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_star_bounds import system_star_bounds
from src.ecs.systems.s_upward_effect import system_upward_effect
from src.ecs.systems.s_movement import system_movement

from src.engine.service_locator import ServiceLocator

class MenuScene(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.load_config()
        self.complete_upward_effect = False

    def load_config(self):
        self.interface = load_interface()
        self.starfield = load_starfield()
        self.window = load_window()

    def do_create(self):
        create_starfield(self.ecs_world, self.starfield, self.screen)
        ServiceLocator.globals_service.score = 0
        draw_text(self.ecs_world, 
                  self.interface["1up"]["value"], 
                  self.interface["1up"]["font"], 
                  self.interface["1up"]["font_size"], 
                  self.interface["1up"]["color"], 
                  self.interface["1up"]["position"],  
                  C_Upward(pygame.Vector2(self.interface["1up"]["position"]["x"], self.interface["1up"]["position"]["y"])))
        draw_text(self.ecs_world, 
                  self.interface["high_score"]["value"], 
                  self.interface["high_score"]["font"], 
                  self.interface["high_score"]["font_size"], 
                  self.interface["high_score"]["color"], 
                  self.interface["high_score"]["position"],  
                  C_Upward(pygame.Vector2(self.interface["high_score"]["position"]["x"], self.interface["high_score"]["position"]["y"])))
        draw_text(self.ecs_world, 
                  self.interface["score_value"]["value"], 
                  self.interface["score_value"]["font"], 
                  self.interface["score_value"]["font_size"], 
                  self.interface["score_value"]["color"], 
                  self.interface["score_value"]["position"],  
                  C_Upward(pygame.Vector2(self.interface["score_value"]["position"]["x"], self.interface["score_value"]["position"]["y"])))
        draw_text(self.ecs_world, 
                  str(ServiceLocator.globals_service.high_score), 
                  self.interface["high_score_value"]["font"], 
                  self.interface["high_score_value"]["font_size"], 
                  self.interface["high_score_value"]["color"], 
                  self.interface["high_score_value"]["position"],  
                  C_Upward(pygame.Vector2(self.interface["high_score_value"]["position"]["x"], self.interface["high_score_value"]["position"]["y"])))
        draw_text(self.ecs_world, 
                  self.interface["start"]["value"], 
                  self.interface["start"]["font"], 
                  self.interface["start"]["font_size"], 
                  self.interface["start"]["color"], 
                  self.interface["start"]["position"], 
                  CBlink(self.interface["start"]["blink_rate"]),
                  C_Upward(pygame.Vector2(self.interface["start"]["position"]["x"], self.interface["start"]["position"]["y"])))
        create_sprite(self.ecs_world, 
                      pygame.Vector2(self.interface["logo_title_img"]["position"]["x"], self.interface["logo_title_img"]["position"]["y"]), pygame.Vector2(0, 0), ServiceLocator.images_service.get(self.interface["logo_title_img"]["image"]),
                      C_Upward(pygame.Vector2(self.interface["logo_title_img"]["position"]["x"], self.interface["logo_title_img"]["position"]["y"])))
        create_menu_input(self.ecs_world)


    def do_update(self, delta_time: float):
        system_blink(self.ecs_world, delta_time)
        system_star_bounds(self.ecs_world, self.screen)
        system_upward_effect(self.ecs_world, self.window["upward_velocity"], self.screen, self.complete_upward_effect, delta_time)
        system_movement(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            if action.phase == CommandPhase.START:
                if not self.complete_upward_effect:
                    self.complete_upward_effect = True
                else:
                    self.switch_scene("LEVEL_01")
