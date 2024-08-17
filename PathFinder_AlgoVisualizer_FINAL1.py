import pygame
import sys
import random
import heapq
from queue import Queue

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

# Initialize pygame
pygame.init()

class Assets:
    def __init__(self):
        self.wall_image = self.load_image("Assets/wall.png")
        self.start_image = self.load_image("Assets/start.png")
        self.stop_image = self.load_image("Assets/stop.png")

    def load_image(self, path):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_maze()

    def generate_maze(self):
        return [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]

    def reset_maze(self):
        self.grid = self.generate_maze()

class Visualizer:
    def __init__(self, screen, maze, assets):
        self.screen = screen
        self.maze = maze
        self.assets = assets
        self.visual_maze = [[0] * COLS for _ in range(ROWS)]

    def draw_maze(self, source, destination):
        self.screen.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                if self.maze.grid[row][col] == 1:
                    self.screen.blit(self.assets.wall_image, (col * CELL_SIZE, row * CELL_SIZE))
                if self.visual_maze[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if self.visual_maze[row][col] == 2:
                    pygame.draw.rect(self.screen, DARKBLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if source and (row, col) == source:
                    self.screen.blit(self.assets.start_image, (col * CELL_SIZE, row * CELL_SIZE))
                if destination and (row, col) == destination:
                    self.screen.blit(self.assets.stop_image, (col * CELL_SIZE, row * CELL_SIZE))
        pygame.display.flip()

    def reset_visual_maze(self):
        self.visual_maze = [[0] * COLS for _ in range(ROWS)]

class Pathfinder:
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, start, goal):
        frontier = [(self.heuristic(start, goal), start)]
        heapq.heapify(frontier)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while frontier:
            current_cost, current = heapq.heappop(frontier)
            if current == goal:
                break
            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current
        path = self.reconstruct_path(came_from, start, goal)
        return path

    def bfs_pathfinding(self, source, destination):
        queue = Queue()
        queue.put(source)
        visited = set()
        visited.add(source)
        bfs_backtrack = {}
        while not queue.empty():
            current = queue.get()
            row, col = current
            if current == destination:
                return bfs_backtrack
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)
                    bfs_backtrack[neighbor] = current
                    self.visualizer.visual_maze[neighbor[0]][neighbor[1]] = 1
                    self.visualizer.draw_maze(source, destination)
                    pygame.time.wait(25)
        return bfs_backtrack

    def dfs_pathfinding(self, current, path=[], source=None, destination=None):
        row, col = current
        if not (0 <= row < ROWS) or not (0 <= col < COLS) or self.maze.grid[row][col] == 1 or self.visualizer.visual_maze[row][col] == 1:
            return None
        if current != source:
            path.append(current)
        self.visualizer.visual_maze[row][col] = 1
        if current == destination:
            return path
        neighbors = self.get_neighbors(current)
        for neighbor in neighbors:
            result = self.dfs_pathfinding(neighbor, path.copy(), source, destination)
            if result:
                return result
        return None

    def get_neighbors(self, cell):
        row, col = cell
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        return [(r, c) for r, c in neighbors if 0 <= r < ROWS and 0 <= c < COLS and self.maze.grid[r][c] == 0]

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        if current not in came_from:
            return None
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def flood_fill(self, source, destination):
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
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.put(neighbor)
                    visited.add(neighbor)
                    self.visualizer.visual_maze[neighbor[0]][neighbor[1]] = 1
            self.visualizer.draw_maze(source, destination)

class MazeSolverGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Solver")
        self.assets = Assets()
        self.maze = Maze(ROWS, COLS)
        self.visualizer = Visualizer(self.screen, self.maze, self.assets)
        self.pathfinder = Pathfinder(self.maze, self.visualizer)
        self.source = None
        self.destination = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
            self.visualizer.draw_maze(self.source, self.destination)
            self.handle_keys()
        pygame.quit()
        sys.exit()

    def handle_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()
        clicked_row = mouse_pos[1] // CELL_SIZE
        clicked_col = mouse_pos[0] // CELL_SIZE
        if event.button == 1:
            if not self.source and self.maze.grid[clicked_row][clicked_col] == 0:
                self.source = (clicked_row, clicked_col)
            elif not self.destination and self.maze.grid[clicked_row][clicked_col] == 0:
                self.destination = (clicked_row, clicked_col)
        elif event.button == 3:
            self.maze.grid[clicked_row][clicked_col] = 0
            self.visualizer.visual_maze[clicked_row][clicked_col] = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.source and self.destination:
            self.visualizer.reset_visual_maze()
            path = self.pathfinder.a_star_search(self.source, self.destination)
            self.animate_path(path)
        if keys[pygame.K_b] and self.source and self.destination:
            self.visualizer.reset_visual_maze()
            bfs_backtrack = self.pathfinder.bfs_pathfinding(self.source, self.destination)
            self.show_bfs_path(bfs_backtrack)
        if keys[pygame.K_d] and self.source and self.destination:
            self.visualizer.reset_visual_maze()
            path = self.pathfinder.dfs_pathfinding(self.source, source=self.source, destination=self.destination)
            self.animate_path(path)
        if keys[pygame.K_f] and self.source and self.destination:
            self.visualizer.reset_visual_maze()
            self.pathfinder.flood_fill(self.source, self.destination)
            self.visualizer.draw_maze(self.source, self.destination)
            pygame.time.wait(2000)
            self.visualizer.reset_visual_maze()
        if keys[pygame.K_r]:
            self.maze.reset_maze()
            self.source = None
            self.destination = None
            self.visualizer.reset_visual_maze()
            self.visualizer.draw_maze(self.source, self.destination)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    def animate_path(self, path):
        if path:
            for i, cell in enumerate(path):
                if i < len(path) - 1:
                    pygame.draw.rect(self.screen, BLUE, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.flip()
                    pygame.time.wait(100)
            pygame.time.wait(2000)
            self.visualizer.reset_visual_maze()

    def show_bfs_path(self, bfs_backtrack):
        if bfs_backtrack:
            pygame.time.wait(1000)
            current = self.destination
            while current != self.source:
                self.visualizer.visual_maze[current[0]][current[1]] = 2
                current = bfs_backtrack[current]
            self.visualizer.draw_maze(self.source, self.destination)
            pygame.time.wait(2000)
            self.visualizer.reset_visual_maze()

if __name__ == "__main__":
    MazeSolverGame().run()