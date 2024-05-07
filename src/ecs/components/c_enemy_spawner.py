class CEnemySpawner:
    def __init__(self, enemy_spawn_events: dict, idle_enemy_velocity: int) -> None:
        self.enemy_spawn_events = enemy_spawn_events
        self.idle_enemy_velocity = idle_enemy_velocity
        self.idle_base_position = 0
        self.spawn_timer = 0
        self.fire_timer = 0
