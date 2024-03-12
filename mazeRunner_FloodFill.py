import pygame
import sys
import random
from queue import Queue

# Define colors
BLACK = (0, 0, 0)
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

# Load images
wall_image = pygame.image.load("Assets/wall.png")
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))

start_image = pygame.image.load("Assets/start.png")
start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

stop_image = pygame.image.load("Assets/stop.png")
stop_image = pygame.transform.scale(stop_image, (CELL_SIZE, CELL_SIZE))

# Create the maze grid
maze = [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Initialize source and destination cells
source = None
destination = None

# Create a copy of the maze for visualization
visual_maze = [[0] * COLS for _ in range(ROWS)]

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flood Fill Maze Solver")

# Function to draw the maze
def draw_maze():
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))
            if visual_maze[row][col] == 1:
                pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif visual_maze[row][col] == 2:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if source and (row, col) == source:
                screen.blit(start_image, (col * CELL_SIZE, row * CELL_SIZE))
            if destination and (row, col) == destination:
                screen.blit(stop_image, (col * CELL_SIZE, row * CELL_SIZE))

    pygame.display.flip()

# Function to run flood fill
def flood_fill():
    queue = Queue()
    queue.put(source)
    visited = set()
    visited.add(source)

    while not queue.empty():
        current = queue.get()
        row, col = current

        if current == destination:
            return

        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                visual_maze[n_row][n_col] = 2  # Mark the cell as part of the visited path

# Main loop
placing_source_destination = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and placing_source_destination:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_SIZE
            clicked_col = mouse_pos[0] // CELL_SIZE

            if event.button == 1:  # Left-click to place source and destination
                if not source and maze[clicked_row][clicked_col] == 0:
                    source = (clicked_row, clicked_col)
                elif not destination and maze[clicked_row][clicked_col] == 0:
                    destination = (clicked_row, clicked_col)

            if source and destination:
                placing_source_destination = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f and source and destination:
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
            flood_fill()
            draw_maze()
            pygame.time.wait(2000)  # Wait for 2 seconds
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

    draw_maze()

    # Check for 'Q' key press to exit
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        running = False

# Keep the window open after the main loop
pygame.quit()
sys.exit()
