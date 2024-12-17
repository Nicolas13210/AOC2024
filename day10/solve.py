
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def get_input(file_path: str):
    with open(file_path, "r") as file:
        return [[int(height) for height in line.strip()] for line in file]
    

def part1(height_map):
    total = 0
    for k in range(0, len(height_map)):
        for i in range(0, len(height_map)):
            if height_map[k][i] == 0:
                trails = solve_recursive(height_map, (k, i),-1)
                trails = set(trails)
                total += len(trails)
    return total

def part2(height_map):
    total = 0
    for k in range(0, len(height_map)):
        for i in range(0, len(height_map)):
            if height_map[k][i] == 0:
                trails = solve_recursive(height_map, (k, i),-1)
                total += len(trails)
    return total

def is_valid_position(height_map, pos):
    return pos[0] >= 0 and pos[0] < len(height_map) and pos[1] >= 0 and pos[1] < len(height_map)


def solve_recursive(height_map, pos,last_value):
    if not is_valid_position(height_map, pos):
        return []
    
    if height_map[pos[0]][pos[1]] - last_value != 1:
        return []
    
    if height_map[pos[0]][pos[1]] == 9:
        return [pos]
    next_positions = []
    new_value = height_map[pos[0]][pos[1]]
    for direction in DIRECTIONS:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        next_positions.append(new_pos)
    return solve_recursive(height_map, next_positions[0], new_value) + solve_recursive(height_map, next_positions[1], new_value) + solve_recursive(height_map, next_positions[2], new_value) + solve_recursive(height_map, next_positions[3], new_value)
    


def solve(file_path: str):
    height_map = get_input(file_path)
    total = part2(height_map)
    print(f'Total: {total}')
    #print(height_map)

solve("day10/input.txt")