
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState

from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_player_ammunition import CTagPlayerAmmunition
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

from src.engine.service_locator import ServiceLocator

def create_square(ecs_world: esper.World, size:pygame.Vector2, pos:pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = ecs_world.create_entity()
    ecs_world.add_component(cuad_entity, CSurface(size, col))
    ecs_world.add_component(cuad_entity, CTransform(pos))
    ecs_world.add_component(cuad_entity, CVelocity(vel))
    return cuad_entity
    
def create_sprite(ecs_world: esper.World, pos: pygame.Vector2, vel:pygame.Vector2, surface:pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity

def create_player_square(ecs_world: esper.World, player: dict, player_spawn: dict) -> int:
    player_sprite = ServiceLocator.images_service.get(player["image"])
    player_entity = create_sprite(
         ecs_world = ecs_world,
         pos = pygame.Vector2(player_spawn["position"]["x"], player_spawn["position"]["y"]),
         vel = pygame.Vector2(0,0),
         surface = player_sprite
    )
    ecs_world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_player_bullet_square(ecs_world: esper.World, bullet: dict, player_pos: pygame.Vector2, player_size: pygame.Vector2):
    bullet_size = pygame.Vector2(bullet["size"]["w"], bullet["size"]["h"])
    bullet_entity = create_square(
         ecs_world = ecs_world,
         size = bullet_size,
         pos = pygame.Vector2(player_pos.x + (player_size[0]/2) - (bullet_size[0]/2), player_pos.y - (bullet_size[1]/2)),
         vel = pygame.Vector2(0, -bullet["velocity"]),
         col = pygame.Color(bullet["color"]["r"], bullet["color"]["g"], bullet["color"]["b"])
    )
    ecs_world.add_component(bullet_entity, CTagPlayerBullet())
    ServiceLocator.sounds_service.play(bullet["sound"])
    return bullet_entity

def create_player_ammunition_square(ecs_world: esper.World, bullet: dict, player_pos: pygame.Vector2, player_size: pygame.Vector2):
    bullet_size = pygame.Vector2(bullet["size"]["w"], bullet["size"]["h"])
    ammunition_entity = create_square(
         ecs_world = ecs_world,
         size = bullet_size,
         pos = pygame.Vector2(player_pos.x + (player_size[0]/2) - (bullet_size[0]/2), player_pos.y - (bullet_size[1]/2)),
         vel = pygame.Vector2(0, 0),
         col = pygame.Color(bullet["color"]["r"], bullet["color"]["g"], bullet["color"]["b"])
    )
    ecs_world.add_component(ammunition_entity, CTagPlayerAmmunition())
    return ammunition_entity

def create_enemy_square(ecs_world: esper.World, enemy: dict, enemy_spawn: dict):
    enemy_sprite = ServiceLocator.images_service.get(enemy["image"])
    size = enemy_sprite.get_size()
    size = (size[0] / enemy["animations"]["number_frames"], size[1])
    enemy_entity = create_sprite(
         ecs_world = ecs_world,
         pos = pygame.Vector2(enemy_spawn["position"]["x"] - (size[0]/2), enemy_spawn["position"]["y"] - (size[1]/2)),
         vel = pygame.Vector2(0, 0),
         surface = enemy_sprite
    )
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CAnimation(enemy["animations"]))
    ecs_world.add_component(enemy_entity, CEnemyState())

def create_input_player(ecs_world: esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_key_space = ecs_world.create_entity()
    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    ecs_world.add_component(input_key_space, CInputCommand("PLAYER_FIRE", pygame.K_SPACE))

def create_enemy_spawner(ecs_world: esper.World, enemy_spawn_events: dict):
    enemy_entity = ecs_world.create_entity()
    ecs_world.add_component(enemy_entity, CEnemySpawner(enemy_spawn_events))

def create_explosion(ecs_world: esper.World, explosion: dict, explosion_pos: pygame.Vector2):
    explosion_sprite = ServiceLocator.images_service.get(explosion["image"])
    explosion_entity = create_sprite(
         ecs_world = ecs_world,
         pos = explosion_pos,
         vel = pygame.Vector2(0,0),
         surface = explosion_sprite
    )
    ecs_world.add_component(explosion_entity, CTagExplosion())
    ecs_world.add_component(explosion_entity, CAnimation(explosion["animations"]))
    ServiceLocator.sounds_service.play(explosion["sound"])
