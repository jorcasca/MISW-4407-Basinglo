from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface

def system_blink(world, delta_time):
    components = world.get_components(CSurface, CBlink)
    for _, (c_s, c_b) in components:
        c_b.blink_timer += delta_time
        if c_b.blink_timer >= c_b.blink_rate:
            c_b.blink_timer = 0
            c_s.toggle_alpha()
