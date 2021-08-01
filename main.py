# Ushno Chakraborty
# A* Pathfinding algorithm visualization
# PEP 8 Format

# HOW TO USE TOOL:
# First left click is start (orange), second left click is endpoint (blue)
# Any point drawn after is a barrier block
# Right click to erase any of the three types of nodes
# If a start or end node is placed then deleted,
# Left clicks will replace the start and end note where the next clicks are
# Press space to run the algorithm and 'c' to clear the board

import pygame
from queue import PriorityQueue

# Window Width
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
# Window Title
pygame.display.set_caption("A* Path Finding Algorithm")

# COLORS
RED = (252, 36, 3)  # Closed
GREEN = (66, 255, 82)  # Open
WHITE = (255, 255, 255)  # Empty Node
BLACK = (0, 0, 0)  # Barrier Node
PURPLE = (128, 0, 128)  # Path
ORANGE = (255, 155, 0)  # Start Node
GREY = (128, 128, 128)  # Lines
TURQUOISE = (64, 224, 208)  # End Node


# A* algorithm loop
def algorithm(draw, grid, start, end):
    count = 0

    # Priority Queue used to denote the open set
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    # Denotes the path of the algorithm
    came_from = {}

    # G score denotes the current distance from the start node
    g = {node: float("inf") for row in grid for node in row}
    g[start] = 0

    # F score is sum of the G score and the H score (heuristic function)
    f = {node: float("inf") for row in grid for node in row}
    f[start] = h(start.get_pos(), end.get_pos())

    # Hash function to store values not in the open set
    open_set_hash = {start}

    # While there are still nodes in the open set
    while not open_set.empty():
        # If the users wishes to quit during the algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Sets current node to node in open set
        current = open_set.get()[2]

        # Removes current node from the open set hash to denote it has been checked
        open_set_hash.remove(current)

        # If the current node is the endpoint, draw the path from the end node to the start
        if current == end:
            reconstruct_path(came_from, end, draw)
            # Redraw start and end nodes for clarity
            end.set_end()
            start.set_start()
            return True

        # Checks each neighbor's validity and adds to open set
        for neighbor in current.neighbors:
            # Since all nodes are distance 1 away from each other
            # Value 1 is added to g to get g of a neighbor
            temp_g = g[current] + 1
            # If g score is lower, add the node to the path
            if temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                # If the neighbor has not been checked, add to open set
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
        draw()

        if current != start:
            current.set_closed()
    # No valid path found, algorithm has no solution
    return False

# Node Refers to the individual cells that set up the map
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Returns node position
    def get_pos(self):
        return self.row, self.col

    # Getter function to check if a node is a barrier
    def get_is_barrier(self):
        return self.color == BLACK

    # Series of setter functions for node state
    def reset(self):
        self.color = WHITE

    def set_start(self):
        self.color = ORANGE

    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def set_barrier(self):
        self.color = BLACK

    def set_end(self):
        self.color = TURQUOISE

    def set_path(self):
        self.color = PURPLE

    # Function to draw node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Function to update the list of the current node's valid neighbors
    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].get_is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].get_is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].get_is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].get_is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])


# Heuristic Function based on Manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# After path is found, reconstructs path from endpoint to start
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


# Functions to draw and map grid
def set_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


# Map mouse click to node
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


# Runs script to visualize algorithm
def main(win, width):
    # Dynamic row value
    ROWS = 50
    grid = set_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # LEFT MOUSE PRESSED
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.set_start()
                elif not end and node != start:
                    end = node
                    end.set_end()
                elif node != end and node != start:
                    node.set_barrier()
            # RIGHT MOUSE PRESSED
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = set_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
