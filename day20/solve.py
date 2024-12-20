from functools import lru_cache
def get_maze(input_file):
    with open(input_file) as f:
        return [list(line) for line in f.read().splitlines()]
    
def get_start(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)

def get_end(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'E':
                return (i, j)
            
def get_path(maze, start, end):
    i = 0
    maze[start[0]][start[1]] = i
    last_position = start
    while start !=end:
        i +=1
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (start[0] + direction[0], start[1] + direction[1])
            if new_position == last_position:
                continue
            elif maze[new_position[0]][new_position[1]] in '.ES':
                maze[new_position[0]][new_position[1]] = i
                last_position = start
                start = new_position

                break
    return maze

def display_maze(maze):
    for row in maze:
        print(''.join(str(cell) for cell in row))

def get_neighbours(maze, position):
    neighbours = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_position = (position[0] + direction[0], position[1] + direction[1])
        if new_position [0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
            continue
        
        neighbours.append(new_position)
    return neighbours

@lru_cache
def rec_shortest_path(maze, start_value,position,num_cheats):
    if num_cheats == 0:
        return 0
    if maze[position[0]][position[1]] != '#':
        #print(f"position: {position}, value: {maze[position[0]][position[1]]}, start_value: {start_value}")
        return start_value - maze[position[0]][position[1]]
    neighbours = get_neighbours(maze, position)
    return max(rec_shortest_path(maze, start_value, neighbour, num_cheats - 1) for neighbour in neighbours)
    
def get_time_saved(maze,position,num_cheats):
    neighbours = [k for k in get_neighbours(maze, position) if maze[k[0]][k[1]] !="#"]
    if len(neighbours) < 2:
        return 1
    start_value = max(maze[position[0]][position[1]] for position in neighbours)
    return rec_shortest_path(maze, start_value, position, num_cheats) -2


def get_time_saved_bis(maze, position):
    neighnours = get_neighbours(maze, position)
    if len(neighnours)< 2:
        return 0
    start = min(neighnours, key = lambda x: maze[x[0]][x[1]])
    end = max(neighnours, key = lambda x: maze[x[0]][x[1]])
    return maze[end[0]][end[1]] - maze[start[0]][start[1]] - 2



def get_all_cheats(maze,num_cheats):
    cheats = {}
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell =="#":
                cheat = get_time_saved(maze, (i, j),num_cheats)
                if not cheat in cheats:
                    cheats[cheat] = 1
                else:
                    cheats[cheat] += 1
    cheats.pop(0, None)
    return cheats

def get_cheats_above_threshold(maze, threshold,num_cheats):
    cheats = get_all_cheats(maze,num_cheats)
    return sum(count for time_saved, count in cheats.items() if time_saved >= threshold)

def solve(input_file,num_cheats):
    maze = get_maze(input_file)
    start = get_start(maze)
    end = get_end(maze)
    solved_maze = get_path(maze, end, start)
    solved_maze = tuple(tuple(row) for row in solved_maze)
    
    total_cheat = get_cheats_above_threshold(solved_maze, 100,num_cheats)
    print(total_cheat)
solve("day20/input.txt",21)