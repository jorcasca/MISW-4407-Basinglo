import asyncio
import pygame

from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene

from src.ecs.components.c_input_command import CInputCommand

from src.utils.load_config import load_window, load_level_01, load_level_02, load_level_03, load_level_04, load_level_05

class GameEngine:
    def __init__(self) -> None:
        self.load_config()
        self.setup_game()

    def load_config(self):
        self.window = load_window()
        self.level_01 = load_level_01()
        self.level_02 = load_level_02()
        self.level_03 = load_level_03()
        self.level_04 = load_level_04()
        self.level_05 = load_level_05()

    def setup_game(self):
        pygame.init()
        pygame.display.set_caption(self.window['title'])
        self.screen = pygame.display.set_mode((self.window['size']['w'], self.window['size']['h']), 0)
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.is_running = False
        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["LEVEL_01"] = PlayScene(self.level_01, self)
        self._scenes["LEVEL_02"] = PlayScene(self.level_02, self)
        self._scenes["LEVEL_03"] = PlayScene(self.level_03, self)
        self._scenes["LEVEL_04"] = PlayScene(self.level_04, self)
        self._scenes["LEVEL_05"] = PlayScene(self.level_05, self)
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None

    async def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.window['framerate'])
        self.delta_time = self.clock.get_time() / 1000.0
    
    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        bg_color = self.window['bg_color']
        self.screen.fill((bg_color['r'], bg_color['g'], bg_color['b']))
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()
