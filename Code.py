import pygame
import random

# --- CONFIG ---
ROWS = 8
COLS = 8
TILE_SIZE = 64
COLORS = [
    (255, 0, 0),    # red
    (0, 255, 0),    # green
    (0, 0, 255),    # blue
    (255, 255, 0),  # yellow
]

pygame.init()
screen = pygame.display.set_mode((COLS*TILE_SIZE, ROWS*TILE_SIZE))
clock = pygame.time.Clock()

# --- Create Board ---
def random_tile():
    return random.randint(0, len(COLORS)-1)

def create_board():
    board = [[random_tile() for _ in range(COLS)] for _ in range(ROWS)]
    return board

board = create_board()
selected = None


# --- Game Logic ---
def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[board[r][c]]
            pygame.draw.rect(screen, color,
                             (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0,0,0),
                             (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)

def swap(pos1, pos2):
    (r1, c1), (r2, c2) = pos1, pos2
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]

def find_matches():
    matched = set()

    # horizontal
    for r in range(ROWS):
        for c in range(COLS-2):
            if board[r][c] == board[r][c+1] == board[r][c+2]:
                matched |= {(r, c), (r, c+1), (r, c+2)}

    # vertical
    for c in range(COLS):
        for r in range(ROWS-2):
            if board[r][c] == board[r+1][c] == board[r+2][c]:
                matched |= {(r, c), (r+1, c), (r+2, c)}

    return matched

def clear_matches(matches):
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


# --- Main Loop ---
running = True
while running:
    clock.tick(60)
    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handle swap clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            r, c = my // TILE_SIZE, mx // TILE_SIZE
            if selected is None:
                selected = (r, c)
            else:
                r2, c2 = r, c
                # only allow adjacent swaps
                if abs(r - selected[0]) + abs(c - selected[1]) == 1:
                    swap(selected, (r2, c2))
                    matches = find_matches()
                    if matches:
                        clear_matches(matches)
                    else:
                        # swap back if no match
                        swap(selected, (r2, c2))
                selected = None

    # board updates each frame
    matches = find_matches()
    if matches:
        clear_matches(matches)
        apply_gravity()
        refill()

    draw_board()
    pygame.display.update()

pygame.quit()
