import pygame
import sys
import random
from queue import Queue

# Define colors
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 153)  # Light Yellow

# Set up maze dimensions and cell size
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Initialize pygame
pygame.init()

# Create the maze grid
maze = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Initialize source and destination cells
source = None
destination = None

# Create a copy of the maze for visualization
visual_maze = [[0] * COLS for _ in range(ROWS)]

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BFS Maze Solver")

# Function to draw the maze
def draw_maze():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = GREY if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if visual_maze[row][col] == 1:
                pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif visual_maze[row][col] == 2:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if source:
        pygame.draw.rect(screen, RED, (source[1] * CELL_SIZE, source[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if destination:
        pygame.draw.rect(screen, GREEN, (destination[1] * CELL_SIZE, destination[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Function to run BFS pathfinding
def bfs_pathfinding():
    queue = Queue()
    queue.put(source)
    visited = set()
    visited.add(source)
    bfs_backtrack = {}  # Dictionary to store the backtrack path

    while not queue.empty():
        current = queue.get()
        row, col = current

        if current == destination:
            return bfs_backtrack

        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                bfs_backtrack[neighbor] = current  # Store the backtrack path
                visual_maze[n_row][n_col] = 1  # Mark the cell as part of the visited path

    return bfs_backtrack

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_SIZE
            clicked_col = mouse_pos[0] // CELL_SIZE

            if not source and maze[clicked_row][clicked_col] == 0:
                source = (clicked_row, clicked_col)
            elif not destination and maze[clicked_row][clicked_col] == 0:
                destination = (clicked_row, clicked_col)

    draw_maze()

    # Highlight the path when key is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_b] and source and destination:
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        bfs_backtrack = bfs_pathfinding()
        if bfs_backtrack:
            pygame.time.wait(2000)  # Wait for 2 seconds before showing the path
            current = destination
            while current != source:
                visual_maze[current[0]][current[1]] = 2  # Mark the cell as part of the BFS path
                current = bfs_backtrack[current]

            draw_maze()
            pygame.time.wait(2000)  # Wait for 2 seconds
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

pygame.quit()
sys.exit()
