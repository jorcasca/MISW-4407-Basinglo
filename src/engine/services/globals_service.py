
class GlobalsService:

    def __init__(self) -> None:
        self.score = 0
        self.high_score = 5000
        self.lifes = 0

    def add_to_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset_score(self):
        self.score = 0

    def set_lifes(self, lifes):
        self.lifes = lifes

    def reduce_life(self):
        self.lifes -= 1
