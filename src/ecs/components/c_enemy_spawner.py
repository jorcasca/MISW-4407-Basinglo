import pygame

class CEnemySpawner:
    def __init__(self, enemy_spawn_events: dict) -> None:
        self.enemy_spawn_events = enemy_spawn_events
        self.spawn_timer = 0
        self.fire_timer = 0