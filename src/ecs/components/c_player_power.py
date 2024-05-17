class CPlayerPower:
    def __init__(self, recharge_duration) -> None:
        self.current_power = 100
        self.elapsed_time = 0
        self.recharge_duration = recharge_duration
