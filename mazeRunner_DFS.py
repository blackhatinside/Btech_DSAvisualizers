import pygame
import sys
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 153)  # Light Yellow
BLUE = (128, 197, 222)

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
pygame.display.set_caption("DFS Maze Solver")

# Function to draw the maze
def draw_maze():
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))
            if visual_maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if source and (row, col) == source:
                screen.blit(start_image, (col * CELL_SIZE, row * CELL_SIZE))
            if destination and (row, col) == destination:
                screen.blit(stop_image, (col * CELL_SIZE, row * CELL_SIZE))

    pygame.display.flip()

# Function to run DFS pathfinding
def dfs_pathfinding(current, path=[]):
    row, col = current
    if not (0 <= row < ROWS) or not (0 <= col < COLS) or maze[row][col] == 1 or visual_maze[row][col] == 1:
        return None
    if current != source:
        path.append(current)
    visual_maze[row][col] = 1  # Mark the cell as part of the visited path

    if current == destination:
        return path

    neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
    for neighbor in neighbors:
        result = dfs_pathfinding(neighbor, path.copy())
        if result:
            return result

    return None

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

            if event.button == 1:  # Left-click to mark source and destination
                if not source and maze[clicked_row][clicked_col] == 0:
                    source = (clicked_row, clicked_col)
                elif not destination and maze[clicked_row][clicked_col] == 0:
                    destination = (clicked_row, clicked_col)
            elif event.button == 3:  # Right-click to delete bricks
                maze[clicked_row][clicked_col] = 0
                visual_maze[clicked_row][clicked_col] = 0

    draw_maze()

    # Highlight the path when key is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and source and destination:
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        path = dfs_pathfinding(source)
        if path:
            for i, cell in enumerate(path):
                if i < len(path) - 1:
                    pygame.draw.rect(screen, BLUE, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.flip()
                    pygame.time.wait(100)  # Wait for 0.1 second
            pygame.time.wait(2000)  # Wait for 2 seconds
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

    # Check for 'Q' key press to exit
    if keys[pygame.K_q]:
        running = False

# Keep the window open after the main loop
pygame.quit()
sys.exit()
