import pygame
import random
import math

pygame.init()

WINDOW_SIZE = (400, 500)
GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE[0] // GRID_SIZE
FPS = 60
ANIMATION_SPEED = 10

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2048")

BACKGROUND_COLOR = (250, 248, 239)
TILE_COLORS = [
    (205, 193, 180), (238, 228, 218), (237, 224, 200), (242, 177, 121),
    (245, 149, 99), (246, 124, 95), (246, 94, 59), (237, 207, 114)
]

clock = pygame.time.Clock()
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0
animations = []

class Animation:
    def __init__(self, start_pos, end_pos, value):
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.current_x, self.current_y = self.start_x, self.start_y
        self.value = value
        self.dx = self.end_x - self.start_x
        self.dy = self.end_y - self.start_y
        self.distance = math.sqrt(self.dx ** 2 + self.dy ** 2)

        if self.distance != 0:
            self.step_x = self.dx / self.distance * ANIMATION_SPEED
            self.step_y = self.dy / self.distance * ANIMATION_SPEED
        else:
            self.step_x = 0
            self.step_y = 0

        self.completed = False

    def update(self):
        self.current_x += self.step_x
        self.current_y += self.step_y

        if (self.dx > 0 and self.current_x >= self.end_x) or (self.dx < 0 and self.current_x <= self.end_x):
            self.current_x = self.end_x
            self.completed = True

        if (self.dy > 0 and self.current_y >= self.end_y) or (self.dy < 0 and self.current_y <= self.end_y):
            self.current_y = self.end_y
            self.completed = True

    def draw(self, surface):
        if self.value > 0:
            color_index = int(math.log2(self.value)) - 1
            tile_color = TILE_COLORS[color_index]
            rect = pygame.Rect(self.current_x, self.current_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, tile_color, rect)
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

def spawn_tile():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = 2 if random.random() < 0.9 else 4

def move_and_merge_tiles(direction):
    global score
    moved = False
    merged = False

    def merge_line(line):
        nonlocal moved, merged
        new_line = [i for i in line if i != 0]
        for i in range(1, len(new_line)):
            if new_line[i] == new_line[i - 1]:
                new_line[i - 1] *= 2
                score += new_line[i - 1]
                new_line[i] = 0
                merged = True
        new_line = [i for i in new_line if i != 0]
        while len(new_line) < GRID_SIZE:
            new_line.append(0)
        return new_line

    def move_line(line):
        nonlocal moved
        new_line = merge_line(line)
        if new_line != line:
            moved = True
        return new_line

    if direction == "left":
        for y in range(GRID_SIZE):
            new_row = move_line([grid[x][y] for x in range(GRID_SIZE)])
            for x in range(GRID_SIZE):
                if grid[x][y] != new_row[x]:
                    animations.append(Animation((x * TILE_SIZE, y * TILE_SIZE), (new_row.index(grid[x][y]) * TILE_SIZE, y * TILE_SIZE), grid[x][y]))
                grid[x][y] = new_row[x]
    elif direction == "right":
        for y in range(GRID_SIZE):
            new_row = move_line([grid[x][y] for x in range(GRID_SIZE - 1, -1, -1)])
            new_row.reverse()
            for x in range(GRID_SIZE):
                if grid[x][y] != new_row[x]:
                    animations.append(Animation((x * TILE_SIZE, y * TILE_SIZE), (GRID_SIZE - 1 - new_row.index(grid[x][y]) * TILE_SIZE, y * TILE_SIZE), grid[x][y]))
                grid[x][y] = new_row[x]
    elif direction == "up":
        for x in range(GRID_SIZE):
            new_col = move_line([grid[x][y] for y in range(GRID_SIZE)])
            for y in range(GRID_SIZE):
                if grid[x][y] != new_col[y]:
                    animations.append(Animation((x * TILE_SIZE, y * TILE_SIZE), (x * TILE_SIZE, new_col.index(grid[x][y]) * TILE_SIZE), grid[x][y]))
                grid[x][y] = new_col[y]
    elif direction == "down":
        for x in range(GRID_SIZE):
            new_col = move_line([grid[x][y] for y in range(GRID_SIZE - 1, -1, -1)])
            new_col.reverse()
            for y in range(GRID_SIZE):
                if grid[x][y] != new_col[y]:
                    animations.append(Animation((x * TILE_SIZE, y * TILE_SIZE), (x * TILE_SIZE, (GRID_SIZE - 1 - new_col.index(grid[x][y])) * TILE_SIZE), grid[x][y]))
                grid[x][y] = new_col[y]

    return moved or merged

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
                color_index = int(math.log2(value)) - 1
                tile_color = TILE_COLORS[color_index]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, tile_color, rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, TILE_COLORS[0], rect)

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
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                moved = move_and_merge_tiles("left")
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                moved = move_and_merge_tiles("right")
            elif event.key in [pygame.K_UP, pygame.K_w]:
                moved = move_and_merge_tiles("up")
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                moved = move_and_merge_tiles("down")
            if moved:
                spawn_tile()
            if not can_move():
                game_over = True

    screen.fill(BACKGROUND_COLOR)
    draw_score()
    draw_grid()
    for animation in animations:
        animation.update()
        animation.draw(screen)
    animations = [anim fora anim in animations if not anim.completed]
    if game_over:
        draw_game_over()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()