import pygame

class FontsService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path:str, size: int) -> pygame.font.Font:
        font_key = (path, size)
        if font_key not in self._fonts:
            self._fonts[path] = pygame.font.Font(path, size)
        return self._fonts[path]
