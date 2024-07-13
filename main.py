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
        grid[x][y] = 2 if random.random() < 0.9 else 4

def slide_tiles(direction):
    moved = False
    for _ in range(GRID_SIZE):
        if direction == "left":
            for y in range(GRID_SIZE):
                row = [grid[x][y] for x in range(GRID_SIZE) if grid[x][y] != 0]
                for x in range(GRID_SIZE):
                    if x < len(row):
                        if grid[x][y] != row[x]:
                            grid[x][y] = row[x]
                            moved = True
                    else:
                        if grid[x][y] != 0:
                            grid[x][y] = 0
                            moved = True
        elif direction == "right":
            for y in range(GRID_SIZE):
                row = [grid[x][y] for x in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
                for x in range(GRID_SIZE-1, -1, -1):
                    if GRID_SIZE-x-1 < len(row):
                        if grid[x][y] != row[GRID_SIZE-x-1]:
                            grid[x][y] = row[GRID_SIZE-x-1]
                            moved = True
                    else:
                        if grid[x][y] != 0:
                            grid[x][y] = 0
                            moved = True
        elif direction == "up":
            for x in range(GRID_SIZE):
                col = [grid[x][y] for y in range(GRID_SIZE) if grid[x][y] != 0]
                for y in range(GRID_SIZE):
                    if y < len(col):
                        if grid[x][y] != col[y]:
                            grid[x][y] = col[y]
                            moved = True
                    else:
                        if grid[x][y] != 0:
                            grid[x][y] = 0
                            moved = True
        elif direction == "down":
            for x in range(GRID_SIZE):
                col = [grid[x][y] for y in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
                for y in range(GRID_SIZE-1, -1, -1):
                    if GRID_SIZE-y-1 < len(col):
                        if grid[x][y] != col[GRID_SIZE-y-1]:
                            grid[x][y] = col[GRID_SIZE-y-1]
                            moved = True
                    else:
                        if grid[x][y] != 0:
                            grid[x][y] = 0
                            moved = True
    return moved

def merge_tiles(direction):
    merged = False
    if direction == "left":
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE-1):
                if grid[x][y] == grid[x+1][y] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    grid[x+1][y] = 0
                    merged = True
    elif direction == "right":
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE-1, 0, -1):
                if grid[x][y] == grid[x-1][y] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    grid[x-1][y] = 0
                    merged = True
    elif direction == "up":
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE-1):
                if grid[x][y] == grid[x][y+1] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    grid[x][y+1] = 0
                    merged = True
    elif direction == "down":
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE-1, 0, -1):
                if grid[x][y] == grid[x][y-1] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    grid[x][y-1] = 0
                    merged = True
    return merged

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
spawn_tile()
spawn_tile()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            moved = False
            if event.key == pygame.K_LEFT:
                moved = slide_tiles("left")
                if moved or merge_tiles("left"):
                    merge_tiles("left")
                    slide_tiles("left")
            elif event.key == pygame.K_RIGHT:
                moved = slide_tiles("right")
                if moved or merge_tiles("right"):
                    merge_tiles("right")
                    slide_tiles("right")
            elif event.key == pygame.K_UP:
                moved = slide_tiles("up")
                if moved or merge_tiles("up"):
                    merge_tiles("up")
                    slide_tiles("up")
            elif event.key == pygame.K_DOWN:
                moved = slide_tiles("down")
                if moved or merge_tiles("down"):
                    merge_tiles("down")
                    slide_tiles("down")
            if moved:
                spawn_tile()

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    pygame.display.flip()

pygame.quit()