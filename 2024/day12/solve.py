import numpy as np
import copy
DIRECTIONS = {(0, 1):"right",(1, 0):"bottom", (0, -1):"left", (-1, 0):"top",(0,0):"Start"}
def get_map_input(input_file):
    with open(input_file) as file:
        data = np.array([[k for k in line.strip()] for line in file.read().splitlines()])
    return data

def replace_values(array, old_value, new_value):
    array[array == old_value] = new_value
    return array


def recursive_solution(data, x, y, farm_type):
    if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
        return np.array([0, 1])  # first index is the area, the second is the perimeter
    if data[x][y] != farm_type and data[x][y] != ".":
        return np.array([0, 1])
    if data[x][y] == ".":
        return np.array([0, 0])
    data[x][y] = "."
    result = np.array([1, 0]) + sum([recursive_solution(data, x + dx, y + dy, farm_type) for dx, dy in DIRECTIONS])
    return result

def part1(data):
    total = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            farm_type = data[i][j]
            if farm_type != "." and farm_type != "#":
                area,perimeter = recursive_solution(data,i,j,farm_type)
                total += area*perimeter
                new_data = replace_values(data, ".", "#")
                data = new_data
    return total

def is_next_to(a,b,orientation):
    if orientation in ["left","right"]:
        return abs(a[0]-b[0]) == 1 and a[1] == b[1]
    else:
        return abs(a[1]-b[1]) == 1 and a[0] == b[0]

def check_sides(position,sides,orientation):
    found = False
    for group in sides[orientation]:
        for side in group:
            if is_next_to(position,side,orientation):
                group.append(position)
                found = True
                break
    if not found:
        sides[orientation].append([position])
    
    
            
def recursive_solution2(data, x, y, farm_type, sides,direction):
    orientation = DIRECTIONS[direction]
    if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
        check_sides((x,y),sides,orientation)
        return 0
    if data[x][y] != farm_type and data[x][y] != ".":
        check_sides((x,y),sides,orientation)
        return 0
    if data[x][y] == ".":
        return 0
    data[x][y] = "."
    result = 1
    for dx, dy in DIRECTIONS:
        result += recursive_solution2(data, x + dx, y + dy, farm_type, sides,(dx,dy))
    return result

def merge_adjacent_groups(sides,orientation):
    new_sides = copy.deepcopy(sides)
    for group in new_sides:
        for side in group:
            for group2 in new_sides:
                if group != group2:
                    for side2 in group2:
                        if is_next_to(side,side2,orientation):
                            group += group2
                            new_sides.remove(group2)
                            break
    return new_sides

def get_total_side_bis(sides):
    total = 0
    for key,value in sides.items():
        for group in value:
            total += len(group)
    return total

def get_total_side(sides):
    new_sides = {}
    for key in sides:
        new_sides[key] = merge_adjacent_groups(sides[key],key)
    total = 0
    for key in new_sides:
        total += len(new_sides[key])
    return total

def part2(data):
    total = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            farm_type = data[i][j]
            if farm_type != "." and farm_type != "#":
                sides = {"top":[],"bottom":[],"left":[],"right":[]}
                area = recursive_solution2(data,i,j,farm_type,sides,(0,0))
                nb_sides = get_total_side(sides)
                print(f"Area: {area} Sides: {nb_sides}, Type: {farm_type}")
                total += area*nb_sides
                new_data = replace_values(data, ".", "#")
                data = new_data
    return total

def solve(input_file: str):
    data = get_map_input(input_file)
    result = part2(data)
    print(f"Result: {result}")
    
solve("day12/input.txt")
#print(is_next_to((3, 4), (3, 3)))