from typing import List

class CEnemySpawner:
    def __init__(self, enemy_spawn_events: dict, idle_enemy_velocity: int) -> None:
        self.enemy_spawn_events: List[CSpawnEvent] = []
        for event in enemy_spawn_events:
            event_data = CSpawnEvent(event["time"], event["enemy_type"], event["position"], False)
            self.enemy_spawn_events.append(event_data)
        self.idle_enemy_velocity = idle_enemy_velocity
        self.idle_base_position = 0
        self.spawn_timer = 0
        self.fire_timer = 0

class CSpawnEvent:
    def __init__(self, time:float, enemy_type:str, position:dict, triggered:bool) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.position = position
        self.triggered = triggered