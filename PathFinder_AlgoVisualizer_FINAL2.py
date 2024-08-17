import pygame
import sys
import random
import heapq
from queue import Queue
from random import choice

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (128, 197, 222)
YELLOW = (255, 255, 153)
DARKBLUE = (0, 0, 255)

# Set up maze dimensions and cell size
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Panel dimensions
PANEL_WIDTH = WIDTH // 2
PANEL_HEIGHT = HEIGHT

# Initialize pygame
pygame.init()

# Load images
wall_image = pygame.image.load("Assets/wall.png")
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))

start_image = pygame.image.load("Assets/start.png")
start_image = pygame.transform.scale(start_image, (CELL_SIZE, CELL_SIZE))

stop_image = pygame.image.load("Assets/stop.png")
stop_image = pygame.transform.scale(stop_image, (CELL_SIZE, CELL_SIZE))

# Function to generate a new maze
def generate_maze():
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Create the maze grid
maze = generate_maze()

# Initialize source and destination cells
source = None
destination = None

# Create a copy of the maze for visualization
visual_maze = [[0] * COLS for _ in range(ROWS)]

# Set up the screen with the panel on the right
screen = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Initialize variables to store the algorithm name and number of explored cells
current_algorithm = None
cells_explored = 0

# Function to draw the panel with details
def draw_panel():
    pygame.draw.rect(screen, BLACK, (WIDTH, 0, PANEL_WIDTH, PANEL_HEIGHT))
    font = pygame.font.Font(None, 32)

    algorithm_text = f"Algorithm: {current_algorithm}"
    cells_explored_text = f"Cells Explored: {cells_explored}"
    start_pos_text = f"Start: {source}"
    end_pos_text = f"End: {destination}"

    text_surface = font.render("MAZE SOLVER", True, WHITE)
    screen.blit(text_surface, (WIDTH + 10, 200))

    text_surface = font.render(algorithm_text, True, WHITE)
    screen.blit(text_surface, (WIDTH + 10, 250))

    text_surface = font.render(cells_explored_text, True, WHITE)
    screen.blit(text_surface, (WIDTH + 10, 300))

    text_surface = font.render(start_pos_text, True, WHITE)
    screen.blit(text_surface, (WIDTH + 10, 350))

    text_surface = font.render(end_pos_text, True, WHITE)
    screen.blit(text_surface, (WIDTH + 10, 400))

# Function to draw the maze
def draw_maze():
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 1:
                screen.blit(wall_image, (col * CELL_SIZE, row * CELL_SIZE))
            if visual_maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if visual_maze[row][col] == 2:
                pygame.draw.rect(screen, DARKBLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if source and (row, col) == source:
                screen.blit(start_image, (col * CELL_SIZE, row * CELL_SIZE))
            if destination and (row, col) == destination:
                screen.blit(stop_image, (col * CELL_SIZE, row * CELL_SIZE))

    # Draw the panel
    draw_panel()

    pygame.display.flip()

def get_neighbors(cell):
    row, col = cell
    neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
    return [(r, c) for r, c in neighbors if 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    if current not in came_from:  # Check if a path exists
        return None
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# A* pathfinding algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal):
    global cells_explored
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
        cells_explored += 1
        for neighbor in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current
    path = reconstruct_path(came_from, start, goal)
    return path

# BFS pathfinding algorithm
def bfs_pathfinding():
    global cells_explored
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
        cells_explored += 1
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                bfs_backtrack[neighbor] = current  # Store the backtrack path
                visual_maze[n_row][n_col] = 1  # Mark the cell as part of the visited path
                draw_maze()
                pygame.time.wait(25)  # Wait for 0.05 second
    return bfs_backtrack

# DFS pathfinding algorithm
def dfs_pathfinding(current, path=[]):
    global cells_explored
    row, col = current
    if not (0 <= row < ROWS) or not (0 <= col < COLS) or maze[row][col] == 1 or visual_maze[row][col] == 1:
        return None
    cells_explored += 1
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

# Flood Fill algorithm
def flood_fill():
    global cells_explored
    if not (source and destination):
        return

    queue = Queue()
    queue.put(source)
    visited = set()
    visited.add(source)

    while not queue.empty():
        current = queue.get()
        row, col = current

        if current == destination:
            return
        cells_explored += 1

        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and maze[n_row][n_col] == 0 and neighbor not in visited:
                queue.put(neighbor)
                visited.add(neighbor)
                visual_maze[n_row][n_col] = 1  # Mark the cell as part of the visited path
        draw_maze()     # animate the flooding

# Main loop
running = True
clock = pygame.time.Clock()
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

    keys = pygame.key.get_pressed()

    # Highlight the A* path when key is pressed
    if keys[pygame.K_a] and source and destination:
        cells_explored = 0
        current_algorithm = "A star"
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        path = a_star_search(source, destination)
        if path:
            for i, cell in enumerate(path):
                if i < len(path) - 1:
                    if cell != source:  # Ensure source is not painted
                        pygame.draw.rect(screen, BLUE, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        pygame.display.flip()
                        # draw_maze()
                        pygame.time.wait(100)  # Wait for 0.1 second
            pygame.time.wait(2000)  # Wait for 2 seconds
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

    # Highlight the BFS path when key is pressed
    if keys[pygame.K_b] and source and destination:
        cells_explored = 0
        current_algorithm = "BFS"
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        bfs_backtrack = bfs_pathfinding()
        if bfs_backtrack:
            pygame.time.wait(1000)  # Wait for 1 second before showing the path
            current = destination
            while current != source:
                visual_maze[current[0]][current[1]] = 2  # Mark the cell as part of the BFS path
                current = bfs_backtrack[current]
            draw_maze()
            pygame.time.wait(2000)  # Wait for 2 seconds
            visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

    # Highlight the DFS path when key is pressed
    if keys[pygame.K_d] and source and destination:
        cells_explored = 0
        current_algorithm = "DFS"
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

    # Highlight the Flood Fill path when key is pressed
    if keys[pygame.K_f] and source and destination:
        cells_explored = 0
        current_algorithm = "Flood Fill"
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Reset the visual maze
        flood_fill()
        draw_maze()
        pygame.time.wait(2000)  # Wait for 2 seconds
        visual_maze = [[0] * COLS for _ in range(ROWS)]  # Clear the path

    # Generate a new maze when the 'R' key is pressed
    if keys[pygame.K_r]:
        cells_explored = 0
        current_algorithm = None
        maze = generate_maze()
        source = None
        destination = None
        visual_maze = [[0] * COLS for _ in range(ROWS)]
        draw_maze()

    pygame.display.flip()

    # Check for 'Q' key press to quit the game
    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    clock.tick(45)     # Framerate

pygame.quit()
sys.exit()  


# DONT CHANGE ANY FEATURE OR BREAK THE CODE, CONVERT IT TO OOP, USE PRIVATE PUBLIC VARIABLES WHEREVER NECESSARY, USE GETTERS, SETTERS, USE DRY/SOLID, USER MODULARITY, USE ABSTRACT METHOD, USE CLASS METHODS, USE @PROPERTY. BUT DONT CHANGE ANY FUNCTIONALITY OR BREAK THE CODE OR DELETE ANY FEATURE. 