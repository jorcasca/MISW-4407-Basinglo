import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color, visible: bool = True) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.visible = visible

    @classmethod
    def from_surface(cls, surface:pygame.Surface):
        c_surf = cls(pygame.Vector2(0,0), pygame.Color(0,0,0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf
    
    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.Color):
        text_surface = font.render(text, True, color)
        return cls.from_surface(text_surface)

    def get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft.copy()
        return new_rect