
class GlobalsService:

    def __init__(self) -> None:
        self.score = 0

    def add_to_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0
