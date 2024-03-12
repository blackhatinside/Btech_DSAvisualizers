import pygame
import sys
import random
import heapq

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
pygame.display.set_caption("A* Maze Solver")

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

# A* pathfinding algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal):
    frontier = [(heuristic(start, goal), start)]
    heapq.heapify(frontier)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current == goal:
            break

        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    path = reconstruct_path(came_from, start, goal)
    return path

def get_neighbors(cell):
    row, col = cell
    neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
    return [(r, c) for r, c in neighbors if 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

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

    # Highlight the A* path when key is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and source and destination:
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        path = a_star_search(source, destination)
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
