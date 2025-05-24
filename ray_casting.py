# raycast 06.06.2024

import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Casting")
clock = pygame.time.Clock()
FPS = 60
WHITE = 'white'
BLACK = 'black'
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

player_pos = [300, HEIGHT // 2]
player_angle = 0
player_speed = 2

FOV = math.pi / 3
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
PROJ_COEFF = 3 * DIST * 50
SCALE = WIDTH // NUM_RAYS

walls = [
    pygame.Rect(100, 100, 200, 20),
    pygame.Rect(400, 100, 20, 200),
    pygame.Rect(100, 400, 200, 20),
    pygame.Rect(400, 400, 20, 200),
    pygame.Rect(250, 250, 300, 20),
    pygame.Rect(500, 300, 20, 200),
    pygame.Rect(200, 150, 20, 200)
]

def draw():
    WIN.fill(GRAY)

    for ray, depth in cast_rays():
        proj_height = PROJ_COEFF / (depth + 0.0001)
        color = DARK_GRAY if depth % 2 else WHITE
        pygame.draw.rect(WIN, color, (ray * SCALE, HEIGHT // 2 - proj_height // 2, SCALE, proj_height))
    
    pygame.display.flip()

def cast_rays():
    rays = []
    start_angle = player_angle - FOV / 2

    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        for depth in range(MAX_DEPTH):
            target_x = player_pos[0] + depth * math.cos(angle)
            target_y = player_pos[1] + depth * math.sin(angle)
            
            if any(wall.collidepoint(target_x, target_y) for wall in walls):
                rays.append((ray, depth))
                break
    
    return rays

def check_collision(pos):
    for wall in walls:
        if wall.collidepoint(pos[0], pos[1]):
            return True
    return False

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    new_pos = player_pos[:]
    if keys[pygame.K_w]:
        new_pos[0] += player_speed * math.cos(player_angle)
        new_pos[1] += player_speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        new_pos[0] -= player_speed * math.cos(player_angle)
        new_pos[1] -= player_speed * math.sin(player_angle)

    if not check_collision(new_pos):
        player_pos = new_pos

    if keys[pygame.K_a]:
        player_angle -= 0.05
    if keys[pygame.K_d]:
        player_angle += 0.05

    draw()
