import pygame
import random
import math

pygame.init()

WINDOW_SIZE = (400, 500)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

BACKGROUND_COLOR = (250, 248, 239)
TILE_COLORS = [(205, 193, 180), (238, 228, 218), (237, 224, 200), (242, 177, 121),
               (245, 149, 99), (246, 124, 95), (246, 94, 59), (237, 207, 114), (119, 221, 119), (135, 206, 250), (255, 182, 193)]

MULTIPLIER_TILE = 1024
CLEAR_ROW_TILE = 2048
CLEAR_COLUMN_TILE = 4096

GRID_SIZE = 4
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0

def spawn_tile():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        tile_type = random.choices([2, 4, MULTIPLIER_TILE, CLEAR_ROW_TILE, CLEAR_COLUMN_TILE],
                                   weights=[80, 15, 1, 2, 2], k=1)[0]
        grid[x][y] = tile_type

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
    global score
    merged = False
    if direction == "left":
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE-1):
                if grid[x][y] == grid[x+1][y] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    score += grid[x][y]
                    grid[x+1][y] = 0
                    merged = True
                elif grid[x][y] == MULTIPLIER_TILE or grid[x+1][y] == MULTIPLIER_TILE:
                    score *= 2
                    grid[x][y] = 0
                    grid[x+1][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_ROW_TILE or grid[x+1][y] == CLEAR_ROW_TILE:
                    for i in range(GRID_SIZE):
                        grid[i][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_COLUMN_TILE or grid[x+1][y] == CLEAR_COLUMN_TILE:
                    for j in range(GRID_SIZE):
                        grid[x][j] = 0
                    merged = True
    elif direction == "right":
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE-1, 0, -1):
                if grid[x][y] == grid[x-1][y] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    score += grid[x][y]
                    grid[x-1][y] = 0
                    merged = True
                elif grid[x][y] == MULTIPLIER_TILE or grid[x-1][y] == MULTIPLIER_TILE:
                    score *= 2
                    grid[x][y] = 0
                    grid[x-1][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_ROW_TILE or grid[x-1][y] == CLEAR_ROW_TILE:
                    for i in range(GRID_SIZE):
                        grid[i][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_COLUMN_TILE or grid[x-1][y] == CLEAR_COLUMN_TILE:
                    for j in range(GRID_SIZE):
                        grid[x][j] = 0
                    merged = True
    elif direction == "up":
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE-1):
                if grid[x][y] == grid[x][y+1] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    score += grid[x][y]
                    grid[x][y+1] = 0
                    merged = True
                elif grid[x][y] == MULTIPLIER_TILE or grid[x][y+1] == MULTIPLIER_TILE:
                    score *= 2
                    grid[x][y] = 0
                    grid[x][y+1] = 0
                    merged = True
                elif grid[x][y] == CLEAR_ROW_TILE or grid[x][y+1] == CLEAR_ROW_TILE:
                    for i in range(GRID_SIZE):
                        grid[i][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_COLUMN_TILE or grid[x][y+1] == CLEAR_COLUMN_TILE:
                    for j in range(GRID_SIZE):
                        grid[x][j] = 0
                    merged = True
    elif direction == "down":
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE-1, 0, -1):
                if grid[x][y] == grid[x][y-1] and grid[x][y] != 0:
                    grid[x][y] *= 2
                    score += grid[x][y]
                    grid[x][y-1] = 0
                    merged = True
                elif grid[x][y] == MULTIPLIER_TILE or grid[x][y-1] == MULTIPLIER_TILE:
                    score *= 2
                    grid[x][y] = 0
                    grid[x][y-1] = 0
                    merged = True
                elif grid[x][y] == CLEAR_ROW_TILE or grid[x][y-1] == CLEAR_ROW_TILE:
                    for i in range(GRID_SIZE):
                        grid[i][y] = 0
                    merged = True
                elif grid[x][y] == CLEAR_COLUMN_TILE or grid[x][y-1] == CLEAR_COLUMN_TILE:
                    for j in range(GRID_SIZE):
                        grid[x][j] = 0
                    merged = True
    return merged

def can_move():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 0:
                return True
            if x < GRID_SIZE - 1 and grid[x][y] == grid[x + 1][y]:
                return True
            if y < GRID_SIZE - 1 and grid[x][y] == grid[x][y + 1]:
                return True
    return False

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = grid[x][y]
            if value > 0:
                color_index = int(math.log2(value)) - 1 if value <= 512 else 8 if value == MULTIPLIER_TILE else 9 if value == CLEAR_ROW_TILE else 10
                tile_color = TILE_COLORS[color_index]
                rect = pygame.Rect(x * 100, y * 100 + 100, 100, 100)
                pygame.draw.rect(screen, tile_color, rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(value) if value <= 512 else "x2" if value == MULTIPLIER_TILE else "R" if value == CLEAR_ROW_TILE else "C", True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def draw_score():
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(WINDOW_SIZE[0] // 2, 50))
    screen.blit(score_text, score_rect)

def draw_game_over():
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(game_over_text, game_over_rect)

running = True
game_over = False
spawn_tile()
spawn_tile()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
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
            if not can_move():
                game_over = True

    screen.fill(BACKGROUND_COLOR)
    draw_score()
    draw_grid()
    if game_over:
        draw_game_over()
    pygame.display.flip()

pygame.quit()