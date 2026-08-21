"""
Pac-Man Clone — Python + Pygame
Arrow keys to move. Eat all dots to win. Avoid the ghosts!
"""

import pygame
import random
import sys

pygame.init()

# ---------- Config ----------
TILE = 24
COLS, ROWS = 21, 21
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + 60
FPS = 60
PLAYER_SPEED = 2
GHOST_SPEED = 2

BLACK = (0, 0, 0)
BLUE = (33, 33, 222)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 184, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
GHOST_COLORS = [RED, PINK, CYAN, ORANGE]

# 1 = wall, 0 = path (dots), 2 = empty path (no dot, e.g. ghost house)
# 21x21 maze layout (symmetric, simplified Pac-Man style)
MAZE = [
    "1111111111111111111",
    "1000000000000000001",
    "1011110111101111101",
    "1010000100001000101",
    "1010111101011101101",
    "1000100000010001001",
    "1110101111101011101",
    "1000101000101000001",
    "1011101011101011101",
    "1010000010000010101",
    "1010111212111101101",
    "1000100222001000001",
    "1110101111101011101",
    "1000001000001000001",
    "1011111101011111101",
    "1010000100001000101",
    "1011010111101011101",
    "1000010000010000001",
    "1111110111011111111",
    "1000000000000000001",
    "1111111111111111111",
]

def load_maze():
    grid = []
    for row in MAZE:
        grid.append([int(c) for c in row])
    return grid

class Entity:
    def __init__(self, x, y, color):
        self.x = x * TILE
        self.y = y * TILE
        self.color = color
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.radius = TILE // 2 - 2

    def grid_pos(self):
        return (round(self.x / TILE), round(self.y / TILE))

    def aligned(self):
        return self.x % TILE == 0 and self.y % TILE == 0

    def can_move(self, grid, dx, dy):
        gx, gy = round(self.x / TILE), round(self.y / TILE)
        nx, ny = gx + dx, gy + dy
        if 0 <= ny < ROWS and 0 <= nx < COLS:
            return grid[ny][nx] != 1
        return False

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, YELLOW)
        self.speed = PLAYER_SPEED

    def update(self, grid):
        if self.aligned():
            if self.can_move(grid, *self.next_dir):
                self.dir = self.next_dir
            if not self.can_move(grid, *self.dir):
                self.dir = (0, 0)
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
        self.x %= COLS * TILE
        self.y %= ROWS * TILE

    def draw(self, screen, frame):
        cx, cy = int(self.x + TILE / 2), int(self.y + TILE / 2 + 60)
        mouth = abs((frame // 5) % 6 - 3) * 10
        angle_map = {(1,0): 0, (-1,0): 180, (0,-1): 90, (0,1): 270, (0,0): 0}
        base_angle = angle_map.get(self.dir, 0)
        if mouth < 5:
            pygame.draw.circle(screen, self.color, (cx, cy), self.radius)
        else:
            start = base_angle + mouth
            end = base_angle - mouth + 360
            pygame.draw.arc(screen, self.color, (cx-self.radius, cy-self.radius, self.radius*2, self.radius*2), 0, 360, 0)
            points = [(cx, cy)]
            import math
            for a in range(int(start), int(end), 5):
                rad = math.radians(a)
                points.append((cx + self.radius * math.cos(rad), cy - self.radius * math.sin(rad)))
            pygame.draw.polygon(screen, self.color, points)

class Ghost(Entity):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.speed = GHOST_SPEED
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def update(self, grid, target):
        if self.aligned():
            gx, gy = round(self.x / TILE), round(self.y / TILE)
            options = []
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                if (dx, dy) == (-self.dir[0], -self.dir[1]):
                    continue
                if self.can_move(grid, dx, dy):
                    options.append((dx, dy))
            if not options:
                options = [(-self.dir[0], -self.dir[1])]
            tx, ty = target
            def dist(d):
                nx, ny = gx + d[0], gy + d[1]
                return (nx - tx) ** 2 + (ny - ty) ** 2
            if random.random() < 0.7:
                options.sort(key=dist)
            else:
                random.shuffle(options)
            self.dir = options[0]
        self.x += self.dir[0] * self.speed
        self.y += self.dir[1] * self.speed
        self.x %= COLS * TILE
        self.y %= ROWS * TILE

    def draw(self, screen):
        cx, cy = int(self.x + TILE / 2), int(self.y + TILE / 2 + 60)
        r = self.radius
        pygame.draw.circle(screen, self.color, (cx, cy - 2), r)
        pygame.draw.rect(screen, self.color, (cx - r, cy - 2, r * 2, r + 4))
        for i in range(4):
            fx = cx - r + i * (r // 2) + r // 4
            pygame.draw.circle(screen, self.color, (fx, cy + r + 2), r // 4)
        for ex in (-r//2, r//2):
            pygame.draw.circle(screen, WHITE, (cx + ex, cy - r//3), 4)
            pygame.draw.circle(screen, BLACK, (cx + ex, cy - r//3), 2)


def draw_maze(screen, grid, dots):
    for y in range(ROWS):
        for x in range(COLS):
            rect = (x * TILE, y * TILE + 60, TILE, TILE)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif (x, y) in dots:
                pygame.draw.circle(screen, WHITE, (x*TILE + TILE//2, y*TILE + TILE//2 + 60), 3)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Clone")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)
    big_font = pygame.font.SysFont("arial", 48, bold=True)

    grid = load_maze()
    dots = set()
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] == 0:
                dots.add((x, y))

    player = Player(10, 15)
    ghosts = [
        Ghost(9, 9, GHOST_COLORS[0]),
        Ghost(10, 9, GHOST_COLORS[1]),
        Ghost(11, 9, GHOST_COLORS[2]),
        Ghost(9, 11, GHOST_COLORS[3]),
    ]

    score = 0
    lives = 3
    frame = 0
    game_over = False
    win = False

    running = True
    while running:
        clock.tick(FPS)
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.next_dir = (0, -1)
                elif event.key == pygame.K_DOWN:
                    player.next_dir = (0, 1)
                elif event.key == pygame.K_LEFT:
                    player.next_dir = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    player.next_dir = (1, 0)
                elif event.key == pygame.K_r and (game_over or win):
                    main()
                    return

        if not game_over and not win:
            player.update(grid)
            pos = player.grid_pos()
            if pos in dots:
                dots.discard(pos)
                score += 10

            for ghost in ghosts:
                ghost.update(grid, player.grid_pos())
                gx, gy = ghost.grid_pos()
                if gx == pos[0] and gy == pos[1]:
                    lives -= 1
                    player.x, player.y = 10 * TILE, 15 * TILE
                    player.dir = (0, 0)
                    for g in ghosts:
                        g.x, g.y = g.x, g.y
                    if lives <= 0:
                        game_over = True

            if not dots:
                win = True

        screen.fill(BLACK)
        draw_maze(screen, grid, dots)
        player.draw(screen, frame)
        for ghost in ghosts:
            ghost.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 15))
        screen.blit(lives_text, (WIDTH - 120, 15))

        if game_over:
            msg = big_font.render("GAME OVER", True, RED)
            sub = font.render("Press R to restart", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))
        elif win:
            msg = big_font.render("YOU WIN!", True, YELLOW)
            sub = font.render("Press R to restart", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()