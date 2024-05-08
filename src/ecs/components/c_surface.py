import pygame

class CSurface:
    def __init__(self, size:pygame.Vector2, color:pygame.Color, visible: bool = True) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()
        self.visible = visible
        self.angle = 0

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

    def update_text(self, text: str, font: pygame.font.Font, color: pygame.Color):
        n_surf = self.from_text(text, font, color)
        self.surf = n_surf.surf
        self.area = n_surf.area

    def get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft.copy()
        return new_rect

    def rotate(self, angle_increment):
        self.angle += angle_increment
        self.angle %= 360
        self.surf = pygame.transform.rotate(self.surf, angle_increment)

    def toggle_alpha(self):
        current_alpha = self.surf.get_alpha()
        new_alpha = 0 if current_alpha == 255 else 255
        self.surf.set_alpha(new_alpha)