from typing import Any


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

def is_unblocked(maze, cell):
    return maze[cell[0]][cell[1]] != "#"

def calculate_h_value(cell, end):
    return abs(cell[0] - end[1]) + abs(cell[0] - end[1])

def trace_path(cell_details,end):
    path = []
    line,column = end
    while not (cell_details[line][column].parent_i != line and cell_details[line][column].parent_j != column):
        path.append((line,column,0))
        temp_line = cell_details[line][column].parent_i
        temp_column = cell_details[line][column].parent_j
        score = cell_details[temp_line][temp_column].g
        line = temp_line
        column = temp_column
    path.append((line,column,score))
    return path

def a_star_search(maze, start, end,ROW,COLUMN):
    closed_list = [[False for _ in range(COLUMN)] for _ in range(ROW)]
    cell_details = [[Cellule() for _ in range(COLUMN)] for _ in range(ROW)]
    i,j = start
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].f = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j
    open_list = [(0,(i,j))]
    found_end = False
    
    while len(open_list)> 0:
        p = open_list.pop(0)
        i,j = p[1]
        closed_list[i][j] = True
        last_direction = cell_details[i][j].last_direction
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        for direction in directions:
            new_i = i + direction[0]
            new_j = j + direction[1]
            if is_unblocked(maze,(new_i,new_j)) and not closed_list[new_i][new_j]:
                if new_i == end[0] and new_j == end[1]:
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("Found the end")
                    print(cell_details[i][j].g +1)
                
                if direction != last_direction:
                    g_new = cell_details[i][j].g + 1001
                else:
                    g_new = cell_details[i][j].g + 1
                direction
                h_new = calculate_h_value((new_i,new_j),end)
                f_new = g_new + h_new
                if cell_details[new_i][new_j].f == float("inf") or cell_details[new_i][new_j].f > f_new:
                    open_list.append((f_new,(new_i,new_j)))
                    cell_details[new_i][new_j].g = g_new
                    cell_details[new_i][new_j].h = h_new
                    cell_details[new_i][new_j].f = f_new
                    cell_details[new_i][new_j].last_direction = direction
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    open_list.sort(key = lambda x: x[0])

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

def get_end(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "E":
                return (i,j)
    return None



                
          
    
def a_star(maze, start, end):
    """TODO"""

def solve(input_file):
    maze = get_maze(input_file)
    start = get_start(maze)
    end = get_end(maze)
    ROW = len(maze)
    COLUMN = len(maze[0])
    path = a_star_search(maze,start,end,ROW,COLUMN)

solve("day16/input.txt")