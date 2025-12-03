import copy
import sys
sys.setrecursionlimit(17385)
def get_map(input_file):
    with open(input_file) as file:
        lines = file.readlines()
    level_map = []
    for i,line in enumerate(lines):
        level_map.append([])
        for char in line.strip():
            level_map[i].append(char)
    return level_map

def get_initial_position(level_map):
    for i,line in enumerate(level_map):
        for j,char in enumerate(line):
            if char == "^":
                return i,j
            

def change_direction(direction):
    if direction == [1,0]:
        return [0,-1]
    if direction == [0,1]:
        return [1,0]
    if direction == [-1,0]:
        return [0,1]
    else:
        return [-1,0]
    
def print_map(level_map):
    for line in level_map:
        print("".join(line))

    print("\n")

def move(i,j,direction,level_map):
    next_i = i + direction[0]
    next_j = j + direction[1]
    # print_map(level_map)
    if next_i < 0 or next_i >= len(level_map) or next_j < 0 or next_j >= len(level_map[0]):
        return 1
    if level_map[next_i][next_j] == ".":
        # print("Moving")
        level_map[i][j] = "X"
        return move(next_i,next_j,direction,level_map) + 1
    if level_map[next_i][next_j] == "#":
        # print("Turning")
        new_direction = change_direction(direction)
        return move(i,j,new_direction,level_map)
    if level_map[next_i][next_j] == "X":
        # print("Backtracking")
        level_map[i][j] = "X"
        return move(next_i,next_j,direction,level_map)
    print("error")
    print(f"map = {level_map}")
    return TypeError

def get_path(i,j,direction,level_map):
    next_i = i + direction[0]
    next_j = j + direction[1]
    # print_map(level_map)
    if next_i < 0 or next_i >= len(level_map) or next_j < 0 or next_j >= len(level_map[0]):
        level_map[i][j] = "X"
        return level_map
    if level_map[next_i][next_j] == ".":
        # print("Moving")
        level_map[i][j] = "X"
        return get_path(next_i,next_j,direction,level_map)
    if level_map[next_i][next_j] == "#":
        # print("Turning")
        new_direction = change_direction(direction)
        return get_path(i,j,new_direction,level_map)
    if level_map[next_i][next_j] == "X":
        # print("Backtracking")
        level_map[i][j] = "X"
        return get_path(next_i,next_j,direction,level_map)
    print("error")
    print(f"map = {level_map}")
    return TypeError

def move_bis(i,j,direction,level_map,history = []):

    if [i,j,direction] in history:
        return 1
    history.append([i,j,direction])
    next_i = i + direction[0]
    next_j = j + direction[1]
    # print_map(level_map)
    if next_i < 0 or next_i >= len(level_map) or next_j < 0 or next_j >= len(level_map[0]):
        
        return 0
    if level_map[next_i][next_j] == ".":
        # print("Moving")
        
        level_map[i][j] = "X"
        return move_bis(next_i,next_j,direction,level_map,history)
    if level_map[next_i][next_j] == "#":
        # print("Turning")
        new_direction = change_direction(direction)
        return move_bis(i,j,new_direction,level_map,history)
    if level_map[next_i][next_j] == "X":
        # print("Backtracking")
        level_map[i][j] = "X"
        return move_bis(next_i,next_j,direction,level_map,history)
    print("error")
    print(f"map = {level_map}")
    return TypeError

def get_all_positions(level_map):
    positions = set()
    for i,line in enumerate(level_map):
        for j,char in enumerate(line):
            if char == "X":
                positions.add((i,j))
    return positions

def get_all_loop(i,j,direction,level_map):
    original_i = i
    original_j = j
    total = 0
    original_map = copy.deepcopy(level_map)
    final_map = get_path(i,j,direction,level_map)
    possible = get_all_positions(final_map)
    for position in possible:
        i,j = position
        if i != original_i or j != original_j:
            temp_map = copy.deepcopy(original_map)
            temp_map[i][j] = "#"
            total += move_bis(original_i,original_j,direction,temp_map,[])

    print(total)



def solve(input_file):
    level_map = get_map(input_file)
    i,j = get_initial_position(level_map)
    direction = [-1,0]
    total = move(i,j,direction,level_map)
    print(f"Total = {total}")

def solve_bis(input_file):
    level_map = get_map(input_file)
    i,j = get_initial_position(level_map)
    direction = [-1,0]
    get_all_loop(i,j,direction,level_map)
    

    
solve_bis("day6/input.txt")