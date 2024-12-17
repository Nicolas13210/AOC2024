from typing import Any
import networkx as nx
import numpy as np

def get_maze(input_file):
    with open(input_file) as file:
        return [[k for k in line] for line in file.read().splitlines()]
    

class Cellule:
    def __init__(self):

        self.parent_i = 0
        self.parent_j = 0
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.last_direction = (0,1)
    def __str__(self) -> str:
        return str(self.g)

def is_unblocked(maze, cell):
    return maze[cell[0]][cell[1]] != "#"

def calculate_h_value(cell, end):
    return abs(cell[0] - end[1]) + abs(cell[0] - end[1])

def trace_path(cell_details, end):
    """
    Trace the path from the end cell to the start cell based on the cell details.

    Args:
        cell_details (list): The details of each cell.
        end (tuple): The coordinates of the end cell.

    Returns:
        list: The path from the end cell to the start cell.
    """
    path = []
    line, column = end
    i = 0
    while cell_details[line][column].parent_i != line or cell_details[line][column].parent_j != column:
        path.append((line, column, 0))
        temp_line = cell_details[line][column].parent_i
        temp_column = cell_details[line][column].parent_j
        score = cell_details[temp_line][temp_column].g
        line = temp_line
        column = temp_column
    path.append((line, column, score))
    return path

def a_star_search(maze, start, end, ROW, COLUMN):
    closed_list = [[False for _ in range(COLUMN)] for _ in range(ROW)]
    cell_details = [[Cellule() for _ in range(COLUMN)] for _ in range(ROW)]
    i, j = start
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].f = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
    open_list = [(0, (i, j))]
    found_end = False

    while len(open_list) > 0:
        p = open_list.pop(0)
        i, j = p[1]
        closed_list[i][j] = True
        last_direction = cell_details[i][j].last_direction
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for direction in directions:
            new_i = i + direction[0]
            new_j = j + direction[1]
            if is_unblocked(maze, (new_i, new_j)) and not closed_list[new_i][new_j]:
                if new_i == end[0] and new_j == end[1]:
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    cell_details[new_i][new_j].g = cell_details[i][j].g + 1
                    print("Found the end")
                    print(cell_details[new_i][new_j].g)
                    continue

                if direction != last_direction:
                    g_new = cell_details[i][j].g + 1001
                else:
                    g_new = cell_details[i][j].g + 1
                h_new = calculate_h_value((new_i, new_j), end)
                f_new = g_new + h_new
                if cell_details[new_i][new_j].f == float("inf") or cell_details[new_i][new_j].f > f_new:
                    open_list.append((f_new, (new_i, new_j)))
                    cell_details[new_i][new_j].g = g_new
                    cell_details[new_i][new_j].h = h_new
                    cell_details[new_i][new_j].f = f_new
                    cell_details[new_i][new_j].last_direction = direction
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    open_list.sort(key=lambda x: x[0])

    return cell_details



def solve_bis(maze,start):
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    i,j = start
    for direction in directions:
        new_i = i + direction[0]
        new_j = j + direction[1]
        if is_unblocked(maze,(new_i,new_j)):
            print(new_i,new_j)
            solve_bis(maze,(new_i,new_j))
    print("End")

def get_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                return (i,j)
    return None

def print_maze(maze):
    
    for line in maze:
        ans = ""
        for cell in line:
            ans += str(cell.g) + "|"
        print(ans)

def create_maze_graph(maze):
    rows, cols = len(maze), len(maze[0])
    G = nx.DiGraph()  # Use a directed graph to handle different costs for different directions
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] != float('inf'):  # Only add nodes for accessible cells
                G.add_node((r, c))
                if r > 0 and maze[r-1][c] != float('inf'):
                    G.add_edge((r, c), (r-1, c), weight=abs(maze[r-1][c] - maze[r][c]))
                if c > 0 and maze[r][c-1] != float('inf'):
                    G.add_edge((r, c), (r, c-1), weight=abs(maze[r][c-1]- maze[r][c]))
                if r < rows - 1 and maze[r+1][c] != float('inf'):
                    G.add_edge((r, c), (r+1, c), weight=abs(maze[r+1][c]- maze[r][c]))
                if c < cols - 1 and maze[r][c+1] != float('inf'):
                    G.add_edge((r, c), (r, c+1), weight=abs(maze[r][c+1]- maze[r][c]))
    return G
        
def find_all_shortest_paths(maze, start, end):
    G = create_maze_graph(maze)
    try:
        # Find the shortest path length using Dijkstra's algorithm
        shortest_path_length = nx.dijkstra_path_length(G, source=start, target=end)
        
        # Find all paths with the shortest path length
        all_paths = list(nx.all_shortest_paths(G, source=start, target=end, weight='weight'))
    except nx.NetworkXNoPath:
        return None
    
    return all_paths

def get_end(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "E":
                return (i,j)
    return None



def get_input_maze(maze):
    return [[cell.g for cell in line] for line in maze]
                
          

def get_unique_tiles(paths):
    unique_tiles = set()
    for path in paths:
        for tile in path:
            unique_tiles.add(tile)
    return unique_tiles
def solve(input_file):
    maze = get_maze(input_file)
    start = get_start(maze)
    end = get_end(maze)
    ROW = len(maze)
    COLUMN = len(maze[0])
    path = a_star_search(maze,start,end,ROW,COLUMN)
    input_maze = get_input_maze(path)
    all_shortest_paths = find_all_shortest_paths(input_maze, start, end)
    unique_tiles = get_unique_tiles(all_shortest_paths)
    print(all_shortest_paths)

    print(len(unique_tiles))
    
maze = get_maze("day16/example.txt")
start = get_start(maze)
end = get_end(maze)
ROW = len(maze)
COLUMN = len(maze[0])
cell_details = a_star_search(maze, start, end, ROW, COLUMN)
shortest_path = trace_path(cell_details, end)
print_maze(cell_details)
print(shortest_path)
# solve("day16/example.txt")