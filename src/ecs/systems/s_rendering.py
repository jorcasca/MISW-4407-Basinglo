
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    for _, (c_t, c_s) in components:
        if c_s.visible:
            screen.blit(c_s.surf, c_t.pos, area=c_s.area)
