import esper
import pygame

from src.ecs.components.c_player_power import CPlayerPower
from src.ecs.components.tags.c_tag_power import CTagPower
from src.ecs.components.c_surface import CSurface

from src.engine.service_locator import ServiceLocator

def system_player_power_recharge(ecs_world: esper.World, interface: dict,  delta_time: float):
    player_component = ecs_world.get_component(CPlayerPower)
    power_component = ecs_world.get_components(CSurface, CTagPower)
    for _, (p_p) in player_component:
        if p_p.current_power < 100:
            p_p.elapsed_time += delta_time
            recharge_rate = 100 / p_p.recharge_duration
            p_p.current_power = min(100, p_p.elapsed_time * recharge_rate)
            color = interface["power_value"]["color_deactivated"]
            if(p_p.current_power == 100):
                color = interface["power_value"]["color_activated"]
            for _, (c_s, _) in power_component:
                c_s.surf = CSurface.from_text(
                    text=f'{int(p_p.current_power)}%',
                    font=ServiceLocator.fonts_service.get(interface["power_value"]["font"], interface["power_value"]["font_size"]),
                    color=pygame.Color(color["r"], color["g"], color["b"])
                ).surf
