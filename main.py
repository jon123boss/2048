import pygame
import random
import math

pygame.init()

WINDOW_SIZE = (400, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

BACKGROUND_COLOR = (250, 248, 239)
TILE_COLORS = [(205, 193, 180), (238, 228, 218), (237, 224, 200), (242, 177, 121),
              (245, 149, 99), (246, 124, 95), (246, 94, 59), (237, 207, 114)]

GRID_SIZE = 4
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def spawn_tile():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = 2

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = grid[x][y]
            if value > 0:
                color_index = int(math.log2(value)) - 1
                tile_color = TILE_COLORS[color_index]
                rect = pygame.Rect(x * 100, y * 100, 100, 100)
                pygame.draw.rect(screen, tile_color, rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    spawn_tile()
    pygame.display.flip()

pygame.quit()
