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

def slide_tiles(direction):
    moved = False
    if direction == "left":
        for y in range(GRID_SIZE):
            row = [grid[x][y] for x in range(GRID_SIZE) if grid[x][y] != 0]
            for x in range(GRID_SIZE):
                if x < len(row):
                    grid[x][y] = row[x]
                else:
                    grid[x][y] = 0
            if row != [grid[x][y] for x in range(GRID_SIZE) if grid[x][y] != 0]:
                moved = True
    elif direction == "right":
        for y in range(GRID_SIZE):
            row = [grid[x][y] for x in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
            for x in range(GRID_SIZE-1, -1, -1):
                if GRID_SIZE-x-1 < len(row):
                    grid[x][y] = row[GRID_SIZE-x-1]
                else:
                    grid[x][y] = 0
            if row != [grid[x][y] for x in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]:
                moved = True
    elif direction == "up":
        for x in range(GRID_SIZE):
            col = [grid[x][y] for y in range(GRID_SIZE) if grid[x][y] != 0]
            for y in range(GRID_SIZE):
                if y < len(col):
                    grid[x][y] = col[y]
                else:
                    grid[x][y] = 0
            if col != [grid[x][y] for y in range(GRID_SIZE) if grid[x][y] != 0]:
                moved = True
    elif direction == "down":
        for x in range(GRID_SIZE):
            col = [grid[x][y] for y in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
            for y in range(GRID_SIZE-1, -1, -1):
                if GRID_SIZE-y-1 < len(col):
                    grid[x][y] = col[GRID_SIZE-y-1]
                else:
                    grid[x][y] = 0
            if col != [grid[x][y] for y in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]:
                moved = True
    return moved

def merge_tiles(direction):
    merged = False
    if direction == "left":
        for y in range(GRID_SIZE):
            row = [grid[x][y] for x in range(GRID_SIZE) if grid[x][y] != 0]
            for x in range(len(row)-1):
                if row[x] == row[x+1]:
                    row[x] *= 2
                    row.pop(x+1)
                    merged = True
            for x in range(GRID_SIZE):
                if x < len(row):
                    grid[x][y] = row[x]
                else:
                    grid[x][y] = 0
    elif direction == "right":
        for y in range(GRID_SIZE):
            row = [grid[x][y] for x in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
            for x in range(len(row)-1):
                if row[x] == row[x+1]:
                    row[x] *= 2
                    row.pop(x+1)
                    merged = True
            for x in range(GRID_SIZE-1, -1, -1):
                if GRID_SIZE-x-1 < len(row):
                    grid[x][y] = row[GRID_SIZE-x-1]
                else:
                    grid[x][y] = 0
    elif direction == "up":
        for x in range(GRID_SIZE):
            col = [grid[x][y] for y in range(GRID_SIZE) if grid[x][y] != 0]
            for y in range(len(col)-1):
                if col[y] == col[y+1]:
                    col[y] *= 2
                    col.pop(y+1)
                    merged = True
            for y in range(GRID_SIZE):
                if y < len(col):
                    grid[x][y] = col[y]
                else:
                    grid[x][y] = 0
    elif direction == "down":
        for x in range(GRID_SIZE):
            col = [grid[x][y] for y in range(GRID_SIZE-1, -1, -1) if grid[x][y] != 0]
            for y in range(len(col)-1):
                if col[y] == col[y+1]:
                    col[y] *= 2
                    col.pop(y+1)
                    merged = True
            for y in range(GRID_SIZE-1, -1, -1):
                if GRID_SIZE-y-1 < len(col):
                    grid[x][y] = col[GRID_SIZE-y-1]
                else:
                    grid[x][y] = 0
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
                if moved:
                    merge_tiles("left")
                    slide_tiles("left")
            elif event.key == pygame.K_RIGHT:
                moved = slide_tiles("right")
                if moved:
                    merge_tiles("right")
                    slide_tiles("right")
            elif event.key == pygame.K_UP:
                moved = slide_tiles("up")
                if moved:
                    merge_tiles("up")
                    slide_tiles("up")
            elif event.key == pygame.K_DOWN:
                moved = slide_tiles("down")
                if moved:
                    merge_tiles("down")
                    slide_tiles("down")
            if moved:
                spawn_tile()

    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    pygame.display.flip()

pygame.quit()