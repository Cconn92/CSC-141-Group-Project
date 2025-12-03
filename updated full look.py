import pygame
import random

# configuration
ROWS = 8
COLS = 8
TILE_SIZE = 64

# Normal candy colors
COLORS = [
    (255, 0, 0),      # red
    (0, 255, 0),      # green
    (0, 0, 255),      # blue
    (255, 255, 0),    # yellow
    (255, 165, 0),    # orange
    (128, 0, 128)     # purple
]

# Bomb color (grey)
BOMB_COLOR = (150, 150, 150)


COLORS.append(BOMB_COLOR)
BOMB_INDEX = len(COLORS) - 1

pygame.init()
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE + 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# board helpers

def random_tile():
    """Spawn normal tiles, but with a small chance of creating a bomb."""
    if random.random() < 0.05:  # 5% bomb chance
        return BOMB_INDEX
    return random.randint(0, BOMB_INDEX - 1)

def create_board():
    return [[random_tile() for _ in range(COLS)] for _ in range(ROWS)]

board = create_board()
selected = None
score = 0

# drawing

def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[board[r][c]]
            pygame.draw.rect(screen, color,
                (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0),
                (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

    # Draw score
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, ROWS*TILE_SIZE + 10))


# game logic

def swap(a, b):
    (r1, c1), (r2, c2) = a, b
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

def explode_bomb(r, c, matched):
    """Add all 8 surrounding tiles to matched set."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            rr, cc = r + dr, c + dc
            if 0 <= rr < ROWS and 0 <= cc < COLS:
                matched.add((rr, cc))

def find_matches():
    """Return a set of all tiles that should be cleared."""
    matched = set()

    # Horizontal matches
    for r in range(ROWS):
        for c in range(COLS - 2):
            a, b, d = board[r][c], board[r][c+1], board[r][c+2]

            # Normal match-3
            if a == b == d:
                matched |= {(r, c), (r, c+1), (r, c+2)}

            # If any part of match contains a bomb
            if BOMB_INDEX in (a, b, d):
                if a == BOMB_INDEX: explode_bomb(r, c, matched)
                if b == BOMB_INDEX: explode_bomb(r, c+1, matched)
                if d == BOMB_INDEX: explode_bomb(r, c+2, matched)

    # Vertical matches
    for c in range(COLS):
        for r in range(ROWS - 2):
            a, b, d = board[r][c], board[r+1][c], board[r+2][c]

            if a == b == d:
                matched |= {(r, c), (r+1, c), (r+2, c)}

            if BOMB_INDEX in (a, b, d):
                if a == BOMB_INDEX: explode_bomb(r, c, matched)
                if b == BOMB_INDEX: explode_bomb(r+1, c, matched)
                if d == BOMB_INDEX: explode_bomb(r+2, c, matched)

    return matched

def clear_matches(matches):
    """Remove matched tiles and add score."""
    global score
    score += len(matches) * 10
    for r, c in matches:
        board[r][c] = None

def apply_gravity():
    for c in range(COLS):
        empty = 0
        for r in range(ROWS-1, -1, -1):
            if board[r][c] is None:
                empty += 1
            elif empty > 0:
                board[r+empty][c] = board[r][c]
                board[r][c] = None

def refill():
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] is None:
                board[r][c] = random_tile()


# main loop

running = True
while running:
    clock.tick(60)
    screen.fill((40, 40, 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if my < ROWS * TILE_SIZE:  # avoid clicking the score area
                r, c = my // TILE_SIZE, mx // TILE_SIZE

                if selected is None:
                    selected = (r, c)
                else:
                    r2, c2 = r, c
                    if abs(r2 - selected[0]) + abs(c2 - selected[1]) == 1:
                        swap(selected, (r2, c2))
                        if not find_matches():  # If no match, undo
                            swap(selected, (r2, c2))
                    selected = None

    # Auto-clear matches every frame
    matches = find_matches()
    if matches:
        clear_matches(matches)
        apply_gravity()
        refill()

    draw_board()
    pygame.display.update()

pygame.quit()


