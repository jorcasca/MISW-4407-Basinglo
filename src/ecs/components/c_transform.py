import pygame

class CTransform:
    def __init__(self, pos:pygame.Vector2) -> None:
        self.pos = pos
        self.initial_pos = pos.copy()
